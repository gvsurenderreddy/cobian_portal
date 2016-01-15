var App = {
	Model: {},		// Model definitions
	Collection: {},	// Colleciton definitions
	View: {},		// View definitions
	Grid: {},		
	termsUploaded: "yes",
	termsAccepted: "no",
}

App.Grid.UserProfileTermColumns = [
	{
	  name: "",
	  cell: "select-row",
	  headerCell: "select-all",
	},
	{
		name: "rep",
		label: "Rep",
		editable: false,
		cell: "string", 
	},
	{
		name: "dealer",
		label: "Dealer",
		editable: false,
		cell: "string", 
	},
	{
		name: "terms_uploaded",
		label: "Terms Uploaded",
		editable: false,
		cell: "string", 
	},
	{
		name: "terms_accepted",
		label: "Terms Accepted",
		editable: false,
		cell: "string", 
	},
	{
		name: "terms_file_path",
		label: "",
		editable: false,
		sortable: false,
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				
				var html = '<a href="' + this.model.attributes.terms_file_path + '" target="_blank"><div class="btn btn-primary btn-xs">View Document</div></a>';
				this.$el.html(html);
				this.delegateEvents();
				return this;
			}
		}),
	},
];

App.Model.UserProfileTerm = Backbone.Model.extend({
	url: "/api/user_profile/term",
});

App.Collection.UserProfileTerms = Backbone.PageableCollection.extend({
	model: App.Model.UserProfileTerm,
	mode: "client",
	url: "/api/user_profile/terms",
	state: {
		pageSize: 20,
	},
});
App.Collection.userProfileTerms = new App.Collection.UserProfileTerms();

// ------------  VIEWS  -----------------
App.View.FilterView = Backbone.View.extend({ 
	el: $(".filter-container"),
	
	events: {
		"change select": "filter",
	},
	
    initialize: function() {

    },
    
	filter: function () {
	    App.termsUploaded = this.$el.find("#terms_uploaded").val();
	    App.termsAccepted = this.$el.find("#terms_accepted").val();
        App.View.gridView.render();
    },
});

App.View.GridView = Backbone.View.extend({ 
	el: $(".grid-container"),
	
	events: {
		"click #accept_selected": "acceptSelected",
	},
	
    initialize: function() {
		this.initialLoad = true;
		this.listenTo(App.Collection.userProfileTerms, "reset", this.showState);
    },
    
    render: function () {
        showLoading();
        App.Collection.userProfileTerms.state.currentPage = 1;
		App.Collection.userProfileTerms.fetch({
			data: $.param({"uploaded": App.termsUploaded, "accepted": App.termsAccepted}),
			reset: true,
		    success: function(data) {
				App.Grid.termsGrid = new Backgrid.Grid({
                    columns: App.Grid.UserProfileTermColumns,
                  	collection: App.Collection.userProfileTerms,
                  	emptyText: "No terms found",
                });
                App.Grid.gridPaginator = new Backgrid.Extension.Paginator({
                  	collection: App.Collection.userProfileTerms
                });
				$("#grid").html(App.Grid.termsGrid.render().$el);
				$("#grid_paginator").html(App.Grid.gridPaginator.render().$el);
		   },
			error: function(jqXHR, textStatus, errorThrown) {
			    $("#grid_info").html("Error getting dealer terms");
				$("#grid").hide();
				$("#grid_paginator").hide();
			}
		}).always(function() { 
			hideLoading();
		});
    },
	
	showState: function(response) {
		var from = ((response.state.currentPage-1) * response.state.pageSize) + 1,
			to = response.state.currentPage * response.state.pageSize;
		
		if (to > response.state.totalRecords) {
			to = response.state.totalRecords;
		}
			
		if (response.state.totalRecords > 0) {
			$("#grid_info").html(from + "-" + to + " of " + response.state.totalRecords);
			$("#grid_info").show();
			$("#grid").show();
			if (response.state.totalRecords > response.state.pageSize) {
				$("#grid_paginator").show();
			} else {
				$("#grid_paginator").hide();
			}
		} else {
			$("#grid_info").hide();
			if (this.initialLoad) {
				$("#grid_filter").hide();
			}
			$("#grid_paginator").hide();
		}
		
		this.initialLoad = false;
	},
	
	acceptSelected: function() {
		var selectedModels = App.Grid.termsGrid.getSelectedModels(),
			acceptCount = 0,
			self = this;
			
		_.each(selectedModels, function(model) {
			model.fetch({
		        data: $.param({"id": model.attributes.id}),
				reset: true,
			    success: function(data) {
					model = data;
				},
				error: function(jqXHR, textStatus, errorThrown) {

				}
			}).always(function() { 
				acceptCount += 1;
				if (acceptCount == selectedModels.length) {
					self.render();
				}
			});
        });
	},
});

$(document).ready(function() {
	App.View.gridView = new App.View.GridView();
	App.View.filterView = new App.View.FilterView();
	
	App.termsUploaded = "yes";
    App.termsAccepted = "no";
    App.View.gridView.render();
});