// ------------------------------------
//             INVENTORY
// ------------------------------------
App.Model.Inventory = Backbone.Model.extend({});
App.Collection.Inventory = Backbone.Collection.extend({
	model: App.Model.Inventory,
	url: "/api/inventory",
});
App.Collection.inventory = new App.Collection.Inventory();

// ------------------------------------
//                ORDER
// ------------------------------------
App.Model.OrderSource = Backbone.Model.extend({});
App.Collection.OrderSources = Backbone.Collection.extend({
	model: App.Model.OrderSource,
	url: "/api/order/sources",
});
App.Collection.orderSources = new App.Collection.OrderSources();

App.Model.PrebookOption = Backbone.Model.extend({});
App.Collection.PrebookOptions = Backbone.Collection.extend({
	model: App.Model.PrebookOption,
	url: "/api/order/prebook/options",
});
App.Collection.preBookOptions = new App.Collection.PrebookOptions();

App.Model.Address = Backbone.Model.extend({});
App.Collection.Addresses = Backbone.Collection.extend({
	model: App.Model.Address,
	url: function() {
		return "/api/user_profiles/" + App.dealerId + "/addresses";
	}
});
App.Collection.addresses = new App.Collection.Addresses();

App.Model.OrderData = Backbone.Model.extend({
	url: "/api/orders/" + App.orderId + "/data",
});
App.Model.orderData = new App.Model.OrderData();

App.Model.Order = Backbone.Model.extend({
	url: "/api/orders/" + App.orderId,
});
App.Model.order = new App.Model.Order();

App.Model.OrderSave = Backbone.Model.extend({
	url: "/api/orders/" + App.orderId + "/save/",
});
App.Model.OrderSubmit = Backbone.Model.extend({
	url: "/api/orders/" + App.orderId + "/submit/",
});
App.Model.orderSubmit = new App.Model.OrderSubmit();
App.Model.OrderDetail = Backbone.Model.extend({
	url: "/api/orders/" + App.orderId + "/details/" + App.orderDetailId,
});
App.Collection.OrderDetails = Backbone.Collection.extend({
	model: App.Model.OrderDetail,
	comparator: "sku"
});
App.Model.orderDetail = new App.Model.OrderDetail();
App.Collection.orderDetails = new App.Collection.OrderDetails();

App.Model.ProductStyle = Backbone.Model.extend({});
App.Collection.ProductStyles = Backbone.Collection.extend({
	model: App.Model.ProductStyle
});
App.Collection.productStyles = new App.Collection.ProductStyles();

// ------------------------------------
//               ORDER
// ------------------------------------
App.View.OrderView = Backbone.View.extend({
    el: $("#order_view"),
    
    events: {
        "change #order_type": "orderTypeChange",
		"change #prebook_date": "prebookDateChange",
		"change input": "inputChange",
		"change select": "inputChange",
    },
	
	initialize: function() {
		var self = this;
		
		this.shipDate = this.$el.find('#ship_date').datepicker({ 
				format: 'mm/dd/yyyy'
			}).on('changeDate', function(ev) {
				self.shipDate.datepicker('hide');
				self.setShipDate();
				App.View.buttonView.enableSave(true);
			});
				
		this.cancelDate = this.$el.find('#cancel_date').datepicker({ 
				format: 'mm/dd/yyyy'
			}).on('changeDate', function(ev) {
				self.cancelDate.datepicker('hide');
				App.View.buttonView.enableSave(true);
			});
	},
	
	render: function() {
		showLoading();
		this.fetchOrderSource();
	},
	
	fetchOrderSource: function(){
        var self = this;
            
		App.Collection.orderSources.fetch({
			reset: true,
		    success: function(data) {
				var html = '';
				if (data.length > 1) {
					html = '<option value="NONE">Select Order Source</option>';
				}
				data.each(function(orderSource) {
					html += '<option value="' + orderSource.attributes.value + '">' + orderSource.attributes.description + '</option>';
				});
				self.$el.find("#order_source").html(html);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				alert(textStatus.responseText);
			}
		}).always(function() { 
			self.fetchPrebookOptions();
		});	
	},
	
	fetchPrebookOptions: function(){
        var self = this;
            
		App.Collection.preBookOptions.fetch({
			reset: true,
		    success: function(data) {
				var html = "";
				data.each(function(preBookOption) {
					html += '<option value="' + preBookOption.attributes.value + '">' + preBookOption.attributes.description + '</option>';
				});
				self.$el.find("#prebook_date").html(html);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				alert(textStatus.responseText);
			}
		}).always(function() { 
			self.fetchOrder();
		});	
	},
	
	fetchOrder: function(){
        var self = this;
            
		App.Model.orderData.fetch({
			reset: true,
		    success: function(data) {
				App.Model.order = new App.Model.Order(data.attributes.order);
				App.Collection.orderDetails.reset(data.attributes.details);
				App.Collection.productStyles.reset(data.attributes.styles);
				
				self.displayOrder();
				self.displayBillTo();
				if (App.Model.order.attributes.status == "NEW") {
					App.View.productStylesView.render();
				} else {
					App.View.orderDetailsView.render();
				}
				self.orderTypeChange();
				self.fetchShipToAddresses();
				App.View.buttonView.render();
			},
			error: function(jqXHR, textStatus, errorThrown) {
				alert(textStatus.responseText);
			}
		}).always(function() { 
			
		});
	},
	
	fetchShipToAddresses: function(){
        var self = this;
            
		App.dealerId = App.Model.order.attributes.dealerId;
		
		App.Collection.addresses.fetch({
			reset: true,
		    success: function(data) {
				var html = "",
					addressId = 0;
				
				data.each(function(address) {
					if (address.attributes.addressType == "SHIPTO") {
						var description = address.attributes.addressId + ' - ' + address.attributes.address1;
						if (address.attributes.address2) {
							description += ', ' + address.attributes.address2;
						}
				        description += ', ' + address.attributes.city + ', ' + address.attributes.state + '&nbsp;&nbsp;' + address.attributes.postalCode;
					
						html += '<option value="' + address.attributes.id + '"';  //>' + description + '</option>';
					
						if (App.Model.order.attributes.shiptoAddress1 == address.attributes.address1 
							&& App.Model.order.attributes.shiptoAddress2 == address.attributes.address2
							&& App.Model.order.attributes.shiptoCity == address.attributes.city
							&& App.Model.order.attributes.shiptoState == address.attributes.state
							&& App.Model.order.attributes.shiptoPostalCode == address.attributes.postalCode) {
								addressId = address.attributes.id;
								html += ' selected';
							}
						html += '>' + description + '</option>';
					}
				});
				self.$el.find("#ship_to").html(html);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				alert(textStatus.responseText);
			}
		}).always(function() { 
			hideLoading();
		});
	},
	
	displayOrder: function() {
		var orderStatus = App.Model.order.attributes.status;
		if (orderStatus == "SUBMIT") {orderStatus = "SUBMITTED";}
		orderStatus += " ORDER";

		this.$el.find('#ship_date').datepicker('update', App.Model.order.attributes.prebookDate);
		this.$el.find('#cancel_date').datepicker('update', App.Model.order.attributes.cancelDate);

		this.$el.find(".order-status").html(orderStatus);
		this.$el.find("#status_date").html(App.Model.order.attributes.statusDate);
		this.$el.find("#po_number").val(App.Model.order.attributes.poNumber);
		this.$el.find("#order_source").val(App.Model.order.attributes.orderSource);
		this.$el.find("#order_type").val(App.Model.order.attributes.orderType);
		this.$el.find("#prebook_date").val(App.Model.order.attributes.prebookOption);
		this.$el.find("#ship_date").val(App.Model.order.attributes.prebookDate);
		this.$el.find("#cancel_date").val(App.Model.order.attributes.cancelDate);
		$("#notes").val(App.Model.order.attributes.notes);
	},
	
	displayBillTo: function() {
        var html = App.Model.order.attributes.billtoName;
		html += " - " + App.Model.order.attributes.billtoAddress1;
		if (App.Model.order.attributes.billtoAddress2) {
			html += ', ' + App.Model.order.attributes.billtoAddress2;
		}
        html += ', ' + App.Model.order.attributes.billtoCity + ', ' + App.Model.order.attributes.billtoState + '&nbsp;&nbsp;' + App.Model.order.attributes.billtoPostalCode;
		this.$el.find("#bill_to").html(html);
	},
	
	inputChange: function(event) {
		App.View.buttonView.enableSave(true);
	}, 
	
	orderTypeChange: function() {
		var orderType = this.$el.find("#order_type").val();
		if (orderType == "PRE-BOOK") {
			this.showInventory(false);
			this.$el.find("#prebook_group").show();
			this.$el.find("#ship_date_group").hide();
			this.$el.find("#cancel_date_group").hide();
		} else {
			this.showInventory(true);
			this.$el.find("#prebook_group").hide();
			this.$el.find("#ship_date_group").show();
			this.$el.find("#cancel_date_group").show();
		}
		this.setShipDate();
	}, 
	
	prebookDateChange: function() {
		this.setShipDate();
	},
	
	setShipDate: function() {
		var orderType = this.$el.find("#order_type").val();
		if (orderType == "PRE-BOOK") {
			App.shipDate = moment($("#prebook_date").val()).unix();
		} else {
			App.shipDate = moment($("#ship_date").val()).unix();
		}
		
	    $.each($('.item-available'), function(index) {
			available = parseInt($(this).data("available"));
			if (App.shipDate >= available) {
				$(this).hide();
			} else {
				$(this).show();
			}
	    });
	
		var skus = "";
	    $.each($('input[type="number"]'), function(index) {
	        var inStock = parseInt($(this).data("instock")),
				available = parseInt($(this).data("available")),
				originalQty = parseInt($(this).data("qty")),
				sku = $(this).data("sku"),
				quantity = $(this).val(),
				disabled = $(this).attr('disabled');
            
			if (App.shipDate >= available && inStock > 0) {
				if (disabled) {
					if (quantity == 0 && originalQty > 0) {
						$(this).val(originalQty);
					}
					$(this).removeAttr("disabled");
				}
			} else {
				if (quantity > 0) {
					skus += "<br>" + sku;
				}
				$(this).val("0");
				if (!disabled) {
					$(this).attr('disabled','disabled');
				}
			}
	    });		 
		
		$.each(App.View.productStylesView.views, function(index) {
			App.View.productStylesView.views[index].displayTotal();
		});	
		this.displayGrandTotal();
		
		if (skus.length > 0) {
			App.View.orderMessageModalView.show("Availability", "There were product styles in the order that are not available by selected ship date.<p>The following skus have been set to zero quantity:" + skus + "</p>");
		}
	},
	
	getOrderType: function() {
		return this.$el.find("#order_type").val();
	},
	
	showInventory: function(show) {
		if (show) {
			$('.product-style input[data-instock="0"]').attr('disabled', 'disabled');
			$('.product-style small').show();
		} else {
			$('.product-style input[type="number"]').removeAttr('disabled');
			$('.product-style small').hide();
		}
	},
	
	displayGrandTotal: function() {
		var grandTotal = 0,
			grandQtyTotal = 0;
			
	    $.each($('.style-total'), function(index) {
			grandTotal += $(this).data("total");
	    });
	    $.each($('.style-qty-total'), function(index) {
			grandQtyTotal += $(this).data("qty-total");
	    });
		
		$('.grand-qty-total').html(grandQtyTotal);
		$('.grand-total').html(accounting.formatMoney(grandTotal));
	}
});

// ------------------------------------
//               NOTES
// ------------------------------------
App.View.NotesView = Backbone.View.extend({
    el: $("#notes_view"),
	
    events: {
        "change textarea": "change",
    },

	change: function(event) {
		App.View.buttonView.enableSave(true);
	}, 
});

// ------------------------------------
//             ORDER DETAILS
// ------------------------------------
App.View.OrderDetailsView = Backbone.View.extend({
    el: $(".panel-group"),
	
	render: function() {
		var orderDetailView = new App.View.OrderDetailView({model: App.Model.order});
		this.$el.append(orderDetailView.render().el);
		
		this.displayGrandTotal();
		
		$("input").attr('disabled','disabled');
		$("select").attr('disabled','disabled');
		$("textarea").attr('disabled','disabled');

	},
	
	displayGrandTotal: function() {
		var grandTotal = 0,
			grandQtyTotal = 0;
			
		App.Collection.orderDetails.each(function(orderDetail) {
			grandTotal += orderDetail.attributes.quantity * orderDetail.attributes.price;
			grandQtyTotal += orderDetail.attributes.quantity;
	    });
		$('.grand-qty-total').html(grandQtyTotal);
		$('.grand-total').html(accounting.formatMoney(grandTotal));
	}
});

App.View.OrderDetailView = Backbone.View.extend({
    template: _.template($('#order_detail_template').html()),
        
    tagName: "div",
	
    className: "panel panel-primary",
	
	render: function() {
        this.$el.html(this.template($.extend(this.model.toJSON(), {orderDetails: App.Collection.orderDetails})));
        return this;
	},

});

App.View.ProductStylesView = Backbone.View.extend({
    el: $(".panel-group"),
	
	initialize: function() {
		this.views = [];
	},
	
	render: function() {
		var self = this;
		App.Collection.productStyles.each(function(productStyle) {
			self.addStyle(productStyle);
		});	
		App.View.orderView.displayGrandTotal();
		
		if (App.Model.order.attributes.status == "NEW") {
			$("#button_view").show();
		} else {
			$("input").attr('disabled','disabled');
			$("select").attr('disabled','disabled');
			$("textarea").attr('disabled','disabled');
		}
	},

	addStyle: function(productStyle) {
		var view = new App.View.ProductStyleView({model: productStyle});
		this.views.push(view);
		this.$el.append(view.render().el);
	},
});

App.View.ProductStyleView = Backbone.View.extend({
    template: _.template($('#product_style_template').html()),
        
    tagName: "div",
	
    className: "panel panel-primary",
	
    events: {
        "change input": "inputChange",
    },
	
	render: function() {
        this.$el.html(this.template($.extend(this.model.toJSON(), {orderDetails: App.Collection.orderDetails, inventory: App.Collection.inventory})));
		this.displayTotal();
        return this;
	},
	
	inputChange: function(event) {
	    var inStock = $(event.currentTarget).data("instock"),
	        quantity = 0,
			orderType = App.View.orderView.getOrderType();
			
		if ($.isNumeric($(event.currentTarget).val())) {
			quantity = parseInt($(event.currentTarget).val());
			if (quantity > inStock && orderType == "AT-ONCE") {
				App.View.orderMessageModalView.show("In Stock Quantity", "Quantity entered is greater than in stock quantity!  Changed quantity from " + quantity + " to " + inStock + ".");
				$(event.currentTarget).val(inStock);
			}
		} else {
			App.View.orderMessageModalView.show("Quantity Error", "Please enter a numeric value for quantity!  Quantity has been set to zero.");
			$(event.currentTarget).val(0);
		}
		
		App.View.buttonView.enableSave(true);
		this.displayTotal();
	}, 
	
	displayTotal: function() {
		var self = this,
			styleTotal = 0,
			styleQtyTotal = 0,
			itemTotal = [];
		
	    $.each(this.$el.find('input'), function(index) {
	        var price = $(this).data("price"),
				itemNumber = $(this).data("itemnumber"),
	            quantity = $(this).val(),
				disabled = $(this).attr('disabled');
                
	        if ($.isNumeric(quantity)) {
				if (!disabled) {
					quantity = parseInt(quantity);
				} else {
					quantity = 0;
				}
				
	        	styleTotal += quantity * price;
				styleQtyTotal += quantity;
				
				if (itemTotal[itemNumber]) {
					itemTotal[itemNumber]["quantity"] += quantity;
					itemTotal[itemNumber]["total"] += quantity * price;
				} else {
					itemTotal[itemNumber] = {
						quantity: quantity,
						total: quantity * price
					}
				}
				self.$el.find(".item-quantity." + itemNumber).html(itemTotal[itemNumber].quantity);
				self.$el.find(".item-total." + itemNumber).html(accounting.formatMoney(itemTotal[itemNumber].total));
	        }
	    });
		
		this.$el.find(".style-qty-total").data("qty-total", styleQtyTotal);
		this.$el.find(".style-qty-total").html(styleQtyTotal);
		
		this.$el.find(".style-total").data("total", styleTotal);
		this.$el.find(".style-total").html(accounting.formatMoney(styleTotal));
		
		App.View.orderView.displayGrandTotal();
	},
});

// ------------------------------------
//             BUTTON VIEW
// ------------------------------------
App.Model.AddProductStyle = Backbone.Model.extend({
	url: function(){
		return "/api/product/styles/" + App.productStyleId + "/detail";
	},
});
App.Model.addProductStyle = new App.Model.AddProductStyle();

App.View.ButtonView = Backbone.View.extend({
    el: $("#button_view"),
	
    events: {
        "click #add_style_button": "addStyle",
		"click #save_button": "save",
		"click #submit_button": "submit",
    },
	
	render: function() {
		if (App.Collection.orderDetails.length > 0) {
			this.$el.find("#submit_button").attr("disabled", false);
		} else {
			this.$el.find("#submit_button").attr("disabled", true);
		}
	},
	
	addStyle: function() {
		var self = this;
		
		App.productStyleId = this.$el.find("select").val();
            
		// Make sure this style is not already loaded...
		var addStyle = true;
	    $.each($('.panel-collapse'), function(index) {
			if ($(this).data("id") == App.productStyleId) {
				addStyle = false;
			}
	    });
		
		if (addStyle) {
			showLoading();
			App.Model.addProductStyle.fetch({
				reset: true,
			    success: function(data) {
					App.View.productStylesView.addStyle(data);
					App.View.orderView.setShipDate();
					
					//$(".panel-collapse.collapse.in").collapse("hide");
					//$("#collapse_" + App.productStyleId).collapse('show');
				},
				error: function(jqXHR, textStatus, errorThrown) {
					alert(textStatus.responseText);
				}
			}).always(function() { 
				hideLoading();
			});	
		}	
	},
	
	enableSave: function(enabled) {
		this.$el.find("#save_button").attr("disabled", !enabled);
		this.$el.find("#submit_button").attr("disabled", enabled);
	},
	
	save: function() {
		var self = this,
			orderSave = new App.Model.OrderSave();
		
		orderSave.attributes.orderId = App.orderId,
		orderSave.attributes.dealerId = App.Model.order.attributes.dealerId,
		orderSave.attributes.poNumber = $("#po_number").val(),
		orderSave.attributes.orderType = $("#order_type").val(),
		orderSave.attributes.orderSource = $("#order_source").val(),
		orderSave.attributes.preBookDate = $("#ship_date").val(),
		orderSave.attributes.cancelDate = $("#cancel_date").val(),
		orderSave.attributes.preBookOption = $("#prebook_date").val(),
		orderSave.attributes.shipToId = $("#ship_to").val(),
		orderSave.attributes.notes = $("#notes").val(),
	    orderSave.attributes.orderItems = [];
		
		if (orderSave.attributes.orderSource == 'NONE') {
			//displayMessage('Order Source', 'Please select an order source.');
			alert('Please select an order source.');
		} else {
		    $.each($('input[type="number"]'), function(index) {
		        var id = $(this).data("id"),
					odid = parseInt($(this).attr("data-odid")),
					originalQty = parseInt($(this).attr("data-qty")),
		            quantity = $(this).val(),
					disabled = $(this).attr('disabled');
                
		        if ($.isNumeric(quantity)) {
		            quantity = parseInt(quantity);
		        } else {
		        	quantity = 0;
		        }
	
				if (quantity > 0 && disabled) {
					quantity = 0;
				}
				
		        if (quantity != originalQty ) {
		            var sku = {
		                id: id,
						odid: odid,
		                quantity: quantity
		            }
		            orderSave.attributes.orderItems.push(sku);
		        }
		    });	
			
	        orderSave.save({}, {
	            wait: true,
			    success: function(model, response) {
					self.setSavedInput(model);
					self.enableSave(false);
				},
				error: function(jqXHR, textStatus, errorThrown) {
	                alert(textStatus.statusText);
				}
			});
		}
	},
	
	setSavedInput: function(model) {
		var self = this
		_.each(model.attributes.orderItems, function(orderItem) {
			$('input[data-id="' + orderItem["id"] + '"]').attr("data-qty", orderItem["quantity"]);
			$('input[data-id="' + orderItem["id"] + '"]').attr("data-odid", orderItem["odid"]);
		});
	},
	
	submit: function() {
		App.View.orderSubmitModalView.show();
	}

});

// ------------------------------------
//         MODAL VIEWS
// ------------------------------------
App.View.OrderMessageModalView = Backbone.View.extend({
    el: $("#order_message_modal"),
	
	show: function(title, message) {
		this.$el.find(".modal-title").html(title);
		this.$el.find(".modal-body p").html(message);
		this.$el.modal("show");
	},
	
	hide: function() {
		this.$el.modal("hide");
	},
});

App.View.OrderSubmitModalView = Backbone.View.extend({
    el: $("#order_submit_modal"),
	
    events: {
		"click #submit_button": "submit",
    },
	
	show: function() {
		this.$el.find(".modal-body p").html("Are you sure you want to submit your order?");
		this.$el.find(".btn").show();
		this.$el.find(".btn-default").html("No");
		this.$el.modal("show");
	},
	
	hide: function() {
		this.$el.modal("hide");
	},
	
	submit: function() {
		var self = this;
		
		self.$el.find(".modal-body p").html("Submitting order...");
		self.$el.find(".btn").hide();
		
		App.Model.orderSubmit.fetch({
			reset: true,
		    success: function(data) {
				window.location.href = "/orders";
			},
			error: function(jqXHR, textStatus, errorThrown) {
				self.$el.find(".modal-body p").html("Error submitting order!");
				self.$el.find(".btn-default").html("Close");
				self.$el.find(".btn-default").show();
			}
		}).always(function() { 
			
		});	
	}

});

// ------------------------------------
//         DOCUMENT READY
// ------------------------------------
$(document).ready(function() {
	Backbone.emulateJSON = true;
	
	showLoading();
	App.Collection.inventory.fetch({
		reset: true,
	    success: function(data) {

		},
		error: function(jqXHR, textStatus, errorThrown) {

		}
	}).always(function() { 
	    App.View.orderView = new App.View.OrderView();
		App.View.notesView = new App.View.NotesView();
		App.View.productStylesView = new App.View.ProductStylesView();
		App.View.orderDetailsView = new App.View.OrderDetailsView();
		App.View.buttonView = new App.View.ButtonView();
		App.View.orderSubmitModalView = new App.View.OrderSubmitModalView();
		App.View.orderMessageModalView = new App.View.OrderMessageModalView();
	    App.View.orderView.render();
	});	
	
});