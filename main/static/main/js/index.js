var App = {
	Model: {},
	Collection: {},
	View: {},
	repId: -1,
	dealerId: 0,
	action: "ORDER"
}

// ------------------------------------
//              MESSAGE
// ------------------------------------
App.View.MessageView = Backbone.View.extend({
    el: $("#message_modal"),
    
    events: {
        "change select": "change"
    },
	
	show: function(title, message) {
		this.$el.find(".modal-title").html(title)
		this.$el.find(".modal-body p").html(message)
		this.$el.modal();
    }
});

// ------------------------------------
//                REPS
// ------------------------------------
App.Model.Rep = Backbone.Model.extend({});
App.Collection.Reps = Backbone.Collection.extend({
	model: App.Model.Rep,
	url: "/api/reps"
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
			html = "";
            
        showLoading();
		App.Collection.reps.fetch({
			reset: true,
		    success: function(data) {
				if (App.Collection.reps.length == 1) {
					App.repId = App.Collection.reps.models[0].attributes.id;
				} else {
					//html = '<option value="-1">Select Rep</option><option value="0">All Reps</option>';
					html = '<option value="0">All Reps</option>';
				}
				
				var repFound = false;
					count = 0,
					repId = 0;
					
				App.Collection.reps.each(function(rep) {
					count++;
					if (count == 1) {
						repId = rep.attributes.id;
					}
					if (rep.attributes.id == App.repId) {
						repFound = true;
					}
					html += '<option value="' + rep.attributes.id + '">' + rep.attributes.accountId + " - " + rep.attributes.name + '</option>';
				});
				if (!repFound) {
					App.repId = repId;
				}
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
    
	show: function () {
		this.$el.show();
	},
	
	hide: function () {
		this.$el.hide();
	},
	
    change: function() {
        App.View.dealerView.reset();
		
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
        var self = this
  	  		html = '';
        
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
					//html = '<option value="-1">Select a Dealer</option><option value="0">All Dealers</option>';
					html = '<option value="0">All Dealers</option>';
				}
				var dealerFound = false;
					count = 0,
					dealerId = 0;
				
				App.Collection.dealers.each(function(dealer) {
					count++;
					if (count == 1) {
						dealerId = dealer.attributes.id;
					}
					if (dealer.attributes.id == App.dealerId) {
						dealerFound = true;
					}
					html += '<option value="' + dealer.attributes.id + '">' + dealer.attributes.accountId + " - " + dealer.attributes.name + '</option>';
				});
				if (!dealerFound) {
					App.dealerId = dealerId;
				}
				
				App.View.actionView.show();
				App.View.buttonView.show();
			},
			error: function(jqXHR, textStatus, errorThrown) {

			}
		}).always(function() { 
		    self.$el.find("select").html(html);
			self.$el.find("select").val(App.dealerId);
			hideLoading();
			
			if (App.Collection.dealers.length == 1) {
				self.hide();
			} else {
				self.show();
			}
		});
	},
	
    reset: function() {
		App.dealerId = -1;
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
		}
    },
	
    getDealerId: function() {
		if (this.$el.find("select").val() > -1) {
		    return parseInt(this.$el.find("select").val());
		} else {
			return 0;
		}
    },
});

// ------------------------------------
//                ACTION
// ------------------------------------
App.View.ActionView = Backbone.View.extend({
    el: $("#action_view"),
    
    events: {
        "change select": "change",
    },
    
	initialize: function(){
		var action = getCookie("action");
		if (action) {
			App.action = action;
		}
		this.$el.find("select").val(App.action);
	},
	
    show: function() {
        this.$el.show();
    },
    
    hide: function() {
        this.$el.hide();
    },
    
    change: function() {
        App.action = this.$el.find("select").val();
    }
});

// ------------------------------------
//                BUTTON
// ------------------------------------
App.Model.NewOrder = Backbone.Model.extend({
	url: "/api/order/new",
});
App.Model.newOrder = new App.Model.NewOrder();

App.View.ButtonView = Backbone.View.extend({
    el: $("#button_view"),
    
    events: {
        "click": "click",
    },
    
	initialize: function(){

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
		setCookie("action", App.action, 30);
		
		if (App.action == "ORDER") {
			this.newOrder();
		} else {
			url = "/orders";
			window.location.assign(url);
		}
		
    },
	
	newOrder: function() {
		if (App.dealerId > 0) {
			App.Model.newOrder.fetch({
				reset: true,
				data: $.param({
					"dealer_id": App.dealerId,
				}),
			    success: function(data) {
					url = "/order/" + data.attributes.id;
					window.location.assign(url);
				},
				error: function(jqXHR, textStatus, errorThrown) {
					App.View.messageView.show("Place Order", "ERROR: " + textStatus.responseText);
				}
			});
		} else {
			App.View.messageView.show("Place Order", "Select a dealer to place an order for.");
		}
	}
});

// ------------------------------------
//           DOCUMENT READY
// ------------------------------------
$(document).ready(function() {
	App.View.messageView = new App.View.MessageView();
    App.View.repView = new App.View.RepView();
    App.View.dealerView = new App.View.DealerView();
	App.View.actionView = new App.View.ActionView();
	App.View.buttonView = new App.View.ButtonView();
	
    App.View.repView.render();
});