var App = {
	Model: {},
	Collection: {},
	View: {},
	Grid: {},
}

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

	},
	
	render: function() {
        var self = this;
        var html = '';
        
        showLoading();
		App.Collection.dealers.fetch({
			reset: true,
			data: $.param({
				"rep_id": 0,
			}),
		    success: function(data) {
				App.Collection.dealers.each(function(dealer) {
					html += '<option value="' + dealer.attributes.id + '">' + dealer.attributes.accountId + " - " + dealer.attributes.name + '</option>';
				});
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		}).always(function() { 
		    self.$el.find("select").html(html);
			self.change();
			hideLoading();
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
			App.View.gridView.render();
		} else {

		}
    },
});

// ------------------------------------
//           MODEL INVENTORY
// ------------------------------------
App.Grid.modelInventoryColumns = [
	{
		name: "modelSku",
		label: "Model Sku",
		editable: false,
		sortType: "toggle",
		direction: "ascending",
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html('<a class="modify">' + this.model.attributes.modelSku + '</a>');
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "modelInventory",
		label: "Model Inventory",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.modelInventory);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "inventorySku",
		label: "Current Sku",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.inventorySku);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "inventory",
		label: "Current Inventory",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.inventory);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "pending",
		label: "Pending Inventory",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.pending);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "threshold",
		label: "Threshold",
		editable: false,
		sortType: "toggle",	
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.threshold);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "active",
		label: "Active",
		editable: false,
		sortType: "toggle",		
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.active);
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
			    var html = '';
				
				html += '<div class="btn btn-danger btn-xs delete">Delete</div>';
			    html += '&nbsp;&nbsp;<div class="btn btn-primary btn-xs duplicate">Duplicate</div>';

                this.$el.empty();
				this.$el.html(html);
				this.delegateEvents();
				return this;
			}
		})
	},
];

App.Model.ModelInventoryCreate = Backbone.Model.extend({
	url: function() {
		return "/api/model/inventory/" + App.dealerId + "/create/";
	}
});
App.Model.ModelInventory = Backbone.Model.extend({});
App.Collection.ModelInventory = Backbone.Collection.extend({
	model: App.Model.ModelInventory,
	url: function() {
		return "/api/model/inventory/" + App.dealerId;
	}
});
App.Collection.modelInventory = new App.Collection.ModelInventory();

App.Grid.modelInventoryRow = Backgrid.Row.extend({
    events: {
        "click .modify": "modify",
		"click .duplicate": "duplicate",
        "click .delete": "delete",
    },
    modify: function () {
        Backbone.trigger("modifyClicked", this.model);
    },
    duplicate: function () {
        Backbone.trigger("duplicateClicked", this.model);
    },
    delete: function () {
        Backbone.trigger("deleteClicked", this.model);
    },
});
Backbone.on("modifyClicked", function (model) {
    App.View.addModifyView.show(model);
});
Backbone.on("duplicateClicked", function (model) {
    App.View.gridView.duplicate(model);
});
Backbone.on("deleteClicked", function (model) {
    App.View.removeView.show(model);
});

App.Grid.modelInventoryFooter = Backgrid.Footer.extend({
  render: function () {
	  this.el.innerHTML = '<tr><td class="renderable" colspan="8" style="text-align: center">Footer data</td></tr>';
	  return this;
  }
});


App.View.GridView = Backbone.View.extend({
    el: $("#grid_container"),
    
    events: {
        "click .btn-success": "add",
    },
	
    render: function () {
        var self = this;
        showLoading();
        
        this.$('#grid_helper').html('Loading model...');
        
        App.Grid.modelInventoryGrid = new Backgrid.Grid({
          	columns: App.Grid.modelInventoryColumns,
          	row: App.Grid.modelInventoryRow,
          	collection: App.Collection.modelInventory,
          	emptyText: "No models found...",
			footer: App.Grid.modelInventoryFooter,
        });
        
        App.Grid.modelInventoryFilter = new simpleFilter({
          collection: App.Collection.modelInventory,
          placeholder: "Search",
          fields: ["modelSku", "inventorySku"],
        });
        
		App.Collection.modelInventory.fetch({
			reset: true,
			//data: $.param({}),
		    success: function(data) {
				self.$('#grid_helper').empty();
				self.$("#grid_filter").html(App.Grid.modelInventoryFilter.render().el);
                self.$("#grid").html(App.Grid.modelInventoryGrid.render().$el);
			},
			error: function(jqXHR, textStatus, errorThrown) {
 				self.$('#grid_helper').html('Error loading models');
			}
		}).always(function() { 
            hideLoading();
		});
    },
	
    add: function() {
		var model = new App.Model.ModelInventoryCreate();
        App.View.addModifyView.show(model);
    },
	
    duplicate: function(model) {
        var self = this;
        model.save("", "", {
            wait: true,
            patch: true,
		    success: function(model, response) {
				self.render();
			},
			error: function(jqXHR, textStatus, errorThrown) {
				self.$('#grid_helper').html('Error duplicating model!');
			}
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

// ------------------------------------
//          ADD/MODIFY MODAL
// ------------------------------------
App.Model.Style = Backbone.Model.extend({});
App.Collection.Styles = Backbone.Collection.extend({
	model: App.Model.Style,
	url: function() {
		return "/api/product/styles";
	}
});
App.Collection.styles = new App.Collection.Styles();

App.Model.Item = Backbone.Model.extend({});
App.Collection.Items = Backbone.Collection.extend({
	model: App.Model.Item,
	url: function() {
		return "/api/product/items/" + App.styleId;
	}
});
App.Collection.items = new App.Collection.Items();

App.Model.Sku = Backbone.Model.extend({});
App.Collection.Skus = Backbone.Collection.extend({
	model: App.Model.Sku,
	url: function() {
		return "/api/product/skus/" + App.itemId;
	}
});
App.Collection.skus = new App.Collection.Skus();

App.View.AddModifyView = Backbone.View.extend({
    el: $("#add_modify_modal"),
    
    events: {
		"change .style select": "styleChange",
		"change .item select": "itemChange",
        "click .btn-success": "save",
    },
    
	initialize: function() {
		var self = this,
			html = '<option value="0" data-style="000">Select Style</option>';
		
		App.Collection.styles.fetch({
			reset: true,
		    success: function(data) {
				App.Collection.styles.each(function(style) {
					html += '<option value="' + style.attributes.id + '" data-style="' + style.attributes.styleSku + '">' + style.attributes.styleSku + ': ' + style.attributes.style + '</option>';
				});
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		}).always(function() { 
		    self.$el.find(".style select").html(html);
		});
	},
	
    styleChange: function() {
		if (this.$el.find(".style select").val() > -1) {
		    App.styleId = parseInt(this.$el.find(".style select").val());
			this.loadItems();
		} else {
		}
    },
	
	loadItems: function() {
		var self = this,
			html = '',
			value = 0;
		
		App.Collection.items.reset();
		App.Collection.items.fetch({
			reset: true,
		    success: function(data) {
				App.Collection.items.each(function(item) {
					if (item.attributes.itemNumber == self.item) {
						value = item.attributes.id;
					}
					html += '<option value="' + item.attributes.id + '" data-item="' + item.attributes.itemNumber + '">' + item.attributes.itemNumber + ': ' + item.attributes.description + '</option>';
				});
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		}).always(function() { 
			if (App.Collection.items.length > 0) {
				self.$el.find(".item").show();
			    self.$el.find(".item select").html(html);
				if (value > 0) {
					self.$el.find(".item select").val(value);
				}
				self.itemChange();
			}
		});
	},
	
    itemChange: function() {
		if (this.$el.find(".item select").val() > -1) {
		    App.itemId = parseInt(this.$el.find(".item select").val());
			this.loadSkus();
		} else {
		}
    },
	
	loadSkus: function() {
		var self = this,
			html = '',
			value = 0;
		
		App.Collection.skus.reset();
		App.Collection.skus.fetch({
			reset: true,
		    success: function(data) {
				App.Collection.skus.each(function(sku) {
					if (sku.attributes.sku == self.sku) {
						value = sku.attributes.id;
					}
					html += '<option value="' + sku.attributes.id + '" data-sku="' + sku.attributes.sku + '">' + sku.attributes.sku + ': ' + sku.attributes.size + '</option>';
				});
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		}).always(function() { 
			if (App.Collection.skus.length > 0) {
				self.$el.find(".sku").show();
			    self.$el.find(".sku select").html(html);
				if (value > 0) {
					self.$el.find(".sku select").val(value);
				}
			}
		});
	},
	
    show: function(model) {
        var title;
		
		this.model = model;
		
		if (model.attributes.id) {
			this.sku = model.attributes.modelSku;
			var skuArray = this.sku.split("-");
			this.style = skuArray[0];
			this.item = skuArray[0] + '-' + skuArray[1];
			title = this.sku;
		} else {
			this.$el.find(".item").hide();
			this.$el.find(".sku").hide();
			this.style = "000";
			this.item = "000-000";
			this.sku = "000-000-000"
			title = "New Model";
			
			this.model.attributes.modelSku = "";
			this.model.attributes.modelInventory = 0;
			this.model.attributes.inventorySku = "";
			this.model.attributes.inventory = 0;
			this.model.attributes.pending = 0;
			this.model.attributes.threshold = 0;
			this.model.attributes.active = false;
		}
		this.$el.find(".modal-title").html(title);
        this.$el.modal();
		this.showStyle();
		this.renderModel();
    },
    
	showStyle: function() {
		var self = this;
		
	    $.each($('.style select option'), function(option) {
			if ($(this).data("style") == self.style) {
				self.$el.find(".style select").val(this.value);
				self.styleChange();
			}
	    });
	},
	
	renderModel: function () {
		$("#model_sku").val(this.model.attributes.modelSku);
		$("#model_inventory").val(this.model.attributes.modelInventory);
		$("#inventory_sku").val(this.model.attributes.inventorySku);
		$("#inventory").val(this.model.attributes.inventory);
		$("#pending").val(this.model.attributes.pending);
		$("#threshold").val(this.model.attributes.threshold);
		$("#active").val(this.model.attributes.active);
	},
	
	validate: function(){
		this.model.attributes.modelSku = $("#model_sku").val();
		this.model.attributes.modelInventory = $("#model_inventory").val();
		this.model.attributes.inventorySku = $("#inventory_sku").val();
		this.model.attributes.inventory = $("#inventory").val();
		this.model.attributes.pending = $("#pending").val();
		this.model.attributes.threshold = $("#threshold").val();
		this.model.attributes.active = $("#active").val();
	},
	
    save: function() {
        var self = this;

		if (this.validate()){
	        model.save({
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
		
    }
});

// ------------------------------------
//            REMOVE MODAL
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

$(document).ready(function() {
    App.View.dealerView = new App.View.DealerView();
	App.View.gridView = new App.View.GridView();
	App.View.addModifyView = new App.View.AddModifyView();
	App.View.removeView = new App.View.RemoveView();
	
	App.View.dealerView.render();
});