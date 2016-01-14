var App = {
	Model: {},
	Collection: {},
	View: {},
	Grid: {},
	repId: -1,
	dealerId: 0,
	type: "ALL",
	status: "ALL",
	dateRange: "ALL",
	startDate: moment().format('l'),
	endDate: moment().format('l'),
	total: 0,
	initial: true,
}

// ------------------------------------
//                REPS
// ------------------------------------
App.Model.Rep = Backbone.Model.extend({});
App.Collection.Reps = Backbone.Collection.extend({
	model: App.Model.Rep,
	url: "/api/reps",
});
App.Collection.reps = new App.Collection.Reps();

App.View.RepView = Backbone.View.extend({
    el: $("#rep_view"),
    
    events: {
        "change select": "change",
    },
	
	initialize: function() {
		var repId = getCookie("repId");
		if (repId) {
			App.repId = parseInt(repId);
		}
	},
	
	render: function() {
        var self = this,
            html = '';
            
        showLoading();
		App.Collection.reps.fetch({
			reset: true,
		    success: function(data) {
				if (App.Collection.reps.length == 1) {
					App.repId = App.Collection.reps.models[0].attributes.id;
				} else {
					html = '<option value="-1">---------------------</option><option value="0">All Reps</option>';
				}
				App.Collection.reps.each(function(rep) {
					html += '<option value="' + rep.attributes.id + '">' + rep.attributes.accountId + " - " + rep.attributes.name + '</option>';
				});
			},
			error: function(jqXHR, textStatus, errorThrown) {
			
			}
		}).always(function() { 
		    self.$el.find("select").html(html);
			self.$el.find("select").val(App.repId);
			hideLoading();
			
			if (App.repId > -1) {
				App.View.dealerView.render();
			}
			
			if (App.Collection.reps.length == 1) {
				self.hide();
			} else {
				self.show();
			}
		});
	},
    
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
	
    change: function() {
        App.View.dealerView.hide();
	    App.View.typeView.hide();
	    App.View.statusView.hide();
	    App.View.dateView.hide();
	    App.View.buttonView.hide();
		//App.View.buttonNewView.hide();
	    App.View.gridView.hide();
	    
		if (this.$el.find("select").val() > -1) {
            App.repId = parseInt(this.$el.find("select").val());
            App.View.dealerView.render();
		} 
    },
});

// ------------------------------------
//                DEALERS
// ------------------------------------
App.Model.Dealer = Backbone.Model.extend({});
App.Collection.Dealers = Backbone.Collection.extend({
	model: App.Model.Dealer,
	url: "/api/dealers",
});
App.Collection.dealers = new App.Collection.Dealers();

App.View.DealerView = Backbone.View.extend({
    el: $("#dealer_view"),
    
    events: {
        "change select": "change",
    },
	
	initialize: function(){
		var dealerId = getCookie("dealerId");
		if (dealerId) {
			App.dealerId = parseInt(dealerId);
		}
		this.$el.find("select").html('<option value="0">All Dealers</option>');
	},
	
	render: function() {
        var self = this;
        var html = '';
        
        showLoading();
		App.Collection.dealers.fetch({
			reset: true,
			data: $.param({
				"rep_id": App.repId,
			}),
		    success: function(data) {
				if (App.Collection.dealers.length == 1) {
					App.dealerId = App.Collection.dealers.models[0].attributes.id;
				} else {
					html = '<option value="-1">---------------------</option><option value="0">All Dealers</option>';
				}
				App.Collection.dealers.each(function(dealer) {
					html += '<option value="' + dealer.attributes.id + '">' + dealer.attributes.accountId + " - " + dealer.attributes.name + '</option>';
				});
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		}).always(function() { 
		    self.$el.find("select").html(html);
			self.$el.find("select").val(App.dealerId);
			self.change();
			hideLoading();
			
			if (App.initial) {
				App.initial = false;
				App.View.gridView.render();
			}
			
			if (App.Collection.dealers.length == 1) {
				self.hide();
			} else {
				self.show();
			}
		});
	},
	
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    change: function() {
		if (this.$el.find("select").val() > -1) {
		    App.dealerId = parseInt(this.$el.find("select").val());
            App.View.typeView.show();
            App.View.statusView.show();
            App.View.dateView.show();
            App.View.buttonView.show();
			//if (this.$el.find("select").val() > 0){
			//	App.View.buttonNewView.show();
			//} else {
			//	App.View.buttonNewView.hide();
			//}
		} else {
            App.View.typeView.hide();
            App.View.statusView.hide();
            App.View.dateView.hide();
            App.View.buttonView.hide();
            App.View.gridView.hide();
			//App.View.buttonNewView.hide();
		}
    },
});

// ------------------------------------
//                TYPE
// ------------------------------------
App.View.TypeView = Backbone.View.extend({
    el: $("#type_view"),
    
    events: {
        "change select": "change",
    },
	
	initialize: function(){
		var type = getCookie("type");
		if (type) {
			App.type = type;
		}
		this.$el.find("select").val(App.type);
	},
	
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    change: function() {
        App.type = this.$el.find("select").val();
    },
});

// ------------------------------------
//                STATUS
// ------------------------------------
App.View.StatusView = Backbone.View.extend({
    el: $("#status_view"),
    
    events: {
        "change select": "change",
    },
	
	initialize: function(){
		var status = getCookie("status");
		if (status) {
			App.status = status;
		}
		this.$el.find("select").val(App.status);
	},
	
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    change: function() {
        App.status = this.$el.find("select").val();
    },
});

// ------------------------------------
//                DATE
// ------------------------------------
App.View.DateView = Backbone.View.extend({
    el: $("#date_view"),
    
    events: {
        "change select": "change",
    },
    
    initialize: function() {
		var dateRange = getCookie("dateRange"),
			startDate = getCookie("startDate"),
			endDate = getCookie("endDate");
		
		if (dateRange) {
			App.dateRange = dateRange;
			App.startDate = startDate;
			App.endDate = endDate;
		}
		this.$el.find("select").val(App.dateRange);
        $('#daterange').val(App.startDate + ' - ' + App.endDate);
		
        $('#daterange').daterangepicker({ 
            timePicker: false, 
            format: 'MM/DD/YYYY',
            ranges: {
                     'Today': [moment(), moment()],
                     'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                     'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                     'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                     'This Month': [moment().startOf('month'), moment().endOf('month')],
                     'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                  },
            startDate: App.startDate,
            endDate: App.endDate,
        });
		
        this.showDateRange();
    },
	
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    showDateRange: function() {
        if (App.dateRange == "ALL") {
            this.$el.find("#daterange").hide();
        } else {
            this.$el.find("#daterange").show();
        }
    },
    
    setDates: function() {
        var dates = $('#daterange').val().split(' - ');
        App.startDate = dates[0];
        App.endDate = dates[1];
		
        setCookie("startDate", App.startDate, 30);
        setCookie("endDate", App.endDate, 30);
    },
    
    change: function() {
        App.dateRange = this.$el.find("select").val();
        this.showDateRange();
    },
});

// ------------------------------------
//                BUTTON
// ------------------------------------
App.View.ButtonView = Backbone.View.extend({
    el: $("#button_view"),
    
    events: {
        "click": "click"
    },
    
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    click: function() {
        setCookie("repId", App.repId, 30);
		setCookie("dealerId", App.dealerId, 30);
		setCookie("type", App.type, 30);
		setCookie("status", App.status, 30);
		setCookie("dateRange", App.dateRange, 30);
        setCookie("startDate", App.startDate, 30);
        setCookie("endDate", App.endDate, 30);
		
        App.View.gridView.render();
    }
});

// ------------------------------------
//           BUTTON NEW
// ------------------------------------
App.View.ButtonNewView = Backbone.View.extend({
    el: $("#button_new_view"),
    
    events: {
        "click": "click"
    },
    
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    click: function() {
        //App.View.gridView.render();
    }
});


// ------------------------------------
//          DUPLICATE ORDER
// ------------------------------------
App.View.DuplicateView = Backbone.View.extend({
    el: $("#duplicate_modal"),
    
    events: {
        "click .btn-primary": "clickYes",
		"click .btn-success": "clickOk",
    },
    
    show: function(model) {
		this.$el.find(".default-message").show();
		this.$el.find(".success-message").hide();
		this.$el.find(".error-message").hide();
		
		this.showOk(false);
        this.model = model;
        this.$el.modal();
    },
    
    clickYes: function() {
        var self = this;
        this.model.save("", "", {
            wait: true,
            patch: true,
		    success: function(model, response) {
				var message = "Order duplicated successfully!";				
				if (response.inactive_skus.length > 0) {
					message = "Order duplicated successfully, but there are inactive skus that could not be duplicated.  The inactive skus are in the notes section of the order.";
				}
				self.$el.find(".default-message").hide();
				self.$el.find(".success-message").html(message);
				self.$el.find(".success-message").show();
				self.showOk(true);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				self.$el.find(".default-message").hide();
				self.$el.find(".error-message").html("Error duplicating order!");
				self.$el.find(".error-message").show();
                self.showOk(true);
			}
		});
    },
	
	showOk: function(display) {
		if (display) {
	 		this.$el.find(".btn-default").hide();
			this.$el.find(".btn-primary").hide();
			this.$el.find(".btn-success").show();
		} else {
			this.$el.find(".btn-default").show();
			this.$el.find(".btn-primary").show();
			this.$el.find(".btn-success").hide();
		}
	},
	
    clickOk: function(model) {
		App.View.gridView.render();
        this.$el.modal('hide');
    }
});

// ------------------------------------
//            REMOVE ORDER
// ------------------------------------
App.View.RemoveView = Backbone.View.extend({
    el: $("#remove_modal"),
    
    events: {
        "click .btn-danger": "click",
    },
    
    show: function(model) {
        this.model = model;
        this.$el.modal();
    },
    
    click: function() {
        var self = this;
        this.model.destroy({
            wait: true,
		    success: function(model, response) {
				App.View.gridView.render();
				self.$el.modal('hide');
			},
			error: function(jqXHR, textStatus, errorThrown) {
                self.$el.modal('hide');
			}
		});
    }
});

// ------------------------------------
//          EMAIL ORDER
// ------------------------------------
App.Model.Email = Backbone.Model.extend({
	url: function() {
		return "/api/order/" + App.emailOrderId + "/email";
	}
});
App.Model.email = new App.Model.Email();

App.View.EmailView = Backbone.View.extend({
    el: $("#email_modal"),

    events: {
        "click .btn-primary": "clickYes",
		"click .btn-success": "clickOk"
    },

    show: function(model) {
        App.emailOrderId = model.attributes.id;

		this.$el.find(".default-message").html('This order will be emailed to yourself.<p>Are you sure you want to email this order to "' + userEmail + '"?</p>');
		this.$el.find(".default-message").show();
		this.$el.find(".success-message").hide();
		this.$el.find(".error-message").hide();

		this.showOk(false);
        this.model = model;
        this.$el.modal();
    },

    clickYes: function() {
        var self = this;
        App.Model.email.fetch({
			reset: true,
		    success: function(data) {
				self.$el.find(".default-message").hide();
				self.$el.find(".success-message").html(data.attributes.message);
				self.$el.find(".success-message").show();
				self.showOk(true);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				self.$el.find(".default-message").hide();
				self.$el.find(".error-message").html("Error emailing order!");
				self.$el.find(".error-message").show();
                self.showOk(true);
			}
		});
    },

	showOk: function(display) {
		if (display) {
	 		this.$el.find(".btn-default").hide();
			this.$el.find(".btn-primary").hide();
			this.$el.find(".btn-success").show();
		} else {
			this.$el.find(".btn-default").show();
			this.$el.find(".btn-primary").show();
			this.$el.find(".btn-success").hide();
		}
	},

    clickOk: function(model) {
        this.$el.modal('hide');
    }
});

// ------------------------------------
//                ORDERS
// ------------------------------------
App.Grid.ordersColumns = [
	{
		name: "orderNumber",
		label: "ORDER #",
		editable: false,
		sortType: "toggle",
		direction: "ascending",
		cell: Backgrid.StringCell.extend({
			render: function () {
				var html = '<a href="order/' + this.model.attributes.orderNumber + '/">' + this.model.attributes.orderNumber + '</a>';
				this.$el.empty();
				this.$el.html(html);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "poNumber",
		label: "PO #",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.poNumber);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "repAccountId",
		label: "REP ACCT",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.repAccountId);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "dealerAccountId",
		label: "DEALER ACCT",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.dealerAccountId);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "dealer",
		label: "DEALER",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.dealer);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "orderDate",
		label: "ORDER DATE",
		editable: false,
		sortType: "toggle",	
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.orderDate);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "status",
		label: "STATUS",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.status);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "statusDate",
		label: "STATUS DATE",
		editable: false,
		sortType: "toggle",	
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.statusDate);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "orderType",
		label: "TYPE",
		editable: false,
		sortType: "toggle",	
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.orderType);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "total",
		label: "TOTAL",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.NumberCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(accounting.formatMoney(this.model.attributes.total));
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		label: "",
		editable: false,
		cell: Backgrid.StringCell.extend({
			render: function () {
			    var html = "";
			    if (this.model.attributes.status == "New Order") {
			        html = '<div class="btn btn-danger btn-sm delete">Delete</div>';
                    html += '<div style="margin-left: 7px" class="btn btn-success btn-sm email">Email</div>';
			    } else {
			        html = '<div class="btn btn-primary btn-sm duplicate">Duplicate</div>';
			    }


                this.$el.empty();
				this.$el.html(html);
				this.delegateEvents();
				return this;
			}
		})
	},
];

App.Model.Order = Backbone.Model.extend({});
App.Collection.Orders = Backbone.ShowMoreCollection.extend({
	model: App.Model.Order,
	mode: "client",
	url: "/api/orders/",
	state: {
		pageSize: 25,
	},

});
App.Collection.orders = new App.Collection.Orders();

App.Grid.orderRow = Backgrid.Row.extend({
    events: {
        "click .duplicate": "duplicate",
        "click .delete": "delete",
        "click .email": "email"
    },
    duplicate: function () {
        Backbone.trigger("duplicateClicked", this.model);
    },
    delete: function () {
        Backbone.trigger("deleteClicked", this.model);
    },
    email: function () {
        //Backbone.trigger("emailClicked", this.model);
        App.View.emailView.show(this.model);
    }
});
Backbone.on("duplicateClicked", function (model) {
    App.View.duplicateView.show(model);
});
Backbone.on("deleteClicked", function (model) {
    App.View.removeView.show(model);
});

App.View.GridView = Backbone.View.extend({
    el: $("#grid_container"),
    
    render: function () {
        App.View.dateView.setDates();
        
        var self = this;
        showLoading();
        
        this.$('#grid_helper').html('Loading orders...');
        
        App.Grid.ordersColumns[2]['renderable'] = App.repId == 0;
        App.Grid.ordersColumns[3]['renderable'] = App.dealerId == 0;
        App.Grid.ordersColumns[4]['renderable'] = App.dealerId == 0;
        App.Grid.ordersColumns[5]['renderable'] = App.dealerId == 0;
        App.Grid.ordersColumns[6]['renderable'] = App.status == "ALL";
        App.Grid.ordersColumns[8]['renderable'] = App.type == "ALL";
        
        App.Grid.ordersGrid = new Backgrid.Grid({
          	columns: App.Grid.ordersColumns,
          	row: App.Grid.orderRow,
          	collection: App.Collection.orders,
          	emptyText: "No orders found",
          	footer: Backgrid.ShowMoreFooter  	
        });
        
        App.Grid.ordersFilter = new simpleFilter({
          collection: App.Collection.orders,
          placeholder: "Search",
          fields: ["orderNumber", "poNumber", "dealer", "repAccountId", "dealerAccountId"],
        });
        
        App.Collection.orders.state.pageSize = 25;
        App.Collection.orders.state.currentPage = 1;
		App.Collection.orders.fetch({
			reset: true,
			data: $.param({
			    "rep_id": App.repId,
			    "dealer_id": App.dealerId,
				"status": App.status,
				"type": App.type,
				"date_range": App.dateRange,
				"start_date": App.startDate,
				"end_date": App.endDate
			}),
		    success: function(data) {
				self.$('#grid_helper').empty();
				self.$("#grid_filter").html(App.Grid.ordersFilter.render().el);
                self.$("#grid").html(App.Grid.ordersGrid.render().$el);
                
                // Calculate grand total
                App.total = 0;
			    App.Collection.orders.fullCollection.each(function(order) {
			        App.total += parseFloat(order.attributes.total);
			    });
			    self.$('#grid_helper').html(accounting.formatMoney(App.total));
			},
			error: function(jqXHR, textStatus, errorThrown) {
 				self.$('#grid_helper').html('Error loading orders');
			}
		}).always(function() { 
		    self.show();
            hideLoading();
		});
    },
	
    show: function () {
        this.$el.show();
    },
	
    hide: function () {
        this.$el.hide();
    },
	
    change: function() {

    },
	

});

$(document).ready(function() {
    App.View.repView = new App.View.RepView();
    App.View.dealerView = new App.View.DealerView();
    App.View.typeView = new App.View.TypeView();
    App.View.statusView = new App.View.StatusView();
    App.View.dateView = new App.View.DateView();
    App.View.buttonView = new App.View.ButtonView();
	//App.View.buttonNewView = new App.View.ButtonNewView();
    App.View.gridView = new App.View.GridView();
    App.View.removeView = new App.View.RemoveView();
    App.View.duplicateView = new App.View.DuplicateView();
    App.View.emailView = new App.View.EmailView();
    
    App.View.repView.render();
});
