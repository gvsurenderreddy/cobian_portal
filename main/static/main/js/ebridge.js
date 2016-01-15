var App = {
	Model: {},		// Model definitions
	Collection: {},	// Colleciton definitions
	View: {},		// View definitions
	Grid: {},		
	docType: "PARTIN",
	status: "New",
	dateRange: "yesterday",
	daysBack: 0
}

App.Grid.eBridgeDocumentColumns = [
    {
      name: "",
      cell: "select-row",
      headerCell: "select-all",
    },
	{
		name: "doc_num",
		label: "Document Num",
		editable: false,
		cell: "string", 
	},
	{
		name: "doc_sys_no",
		label: "System Number",
		editable: false,
		cell: "string", 
	},
	{
		name: "tran_datetime",
		label: "Transaction Date",
		editable: false,
		cell: "string", 
	},
	{
		name: "doc_date",
		label: "Document Date",
		editable: false,
		cell: "string", 
	},
];

App.Model.eBridgeDocument = Backbone.Model.extend({
	url: "/api/ebridge/document",
});

App.Collection.eBridgeDocuments = Backbone.PageableCollection.extend({
	model: App.Model.eBridgeDocument,
	mode: "client",
	url: "/api/ebridge/documents",
	state: {
		pageSize: 20,
	},
});
App.Collection.documents = new App.Collection.eBridgeDocuments();

// ------------  VIEWS  -----------------

App.View.ImportView = Backbone.View.extend({ 
	el: $("#import_modal"),
	
	events: {
		"click .btn-default": "close",
	},
	
    initialize: function() {
		this.$el.find(".progress-bar").css("width", "0%");
		this.$el.find(".btn-default").hide();
		this.$el.find(".success-count span").html("");
		this.$el.find(".error-count span").html("");
		this.$el.find(".error-message").html("");
		
		var title = "Importing Documents";
		switch (App.doc_type) {
			case "INVRPT":
				title = "Importing Products";
				break;
			
			case "PARTIN":
				title = "Importing Partners";
				break;
		} 
		this.$el.find(".modal-title").html(title);
		this.$el.modal({
          keyboard: false,
          backdrop: "static",
        });
		this.importDocuments();
    },
    
    close: function () {
		this.$el.modal("hide");
		if (App.doc_status == "New") {
			App.View.documentView.render();
		}
    },
    
	importDocuments: function () {
		this.totalDocuments = App.selectedModels.length;
		this.totalCount = 0;
		this.successCount = 0;
		this.errorCount = 0;
		
		this.$el.find(".success-count span").html(this.successCount);
		this.$el.find(".error-count span").html(this.errorCount);
		
		this.importDocument();
		
		/*
		_.each(App.selectedModels, function(document) {
			document.fetch({
		        data: $.param({"doc_type": App.doc_type, "doc_sys_no": document.attributes.doc_sys_no}),
				reset: true,
			    success: function(data) {
					successCount += 1;
					if (App.doc_type == "PARTIN") {
						self.$el.find(".success-count span").html(successCount + " - Rep: " + data.attributes.rep_id + "  Partner: " + data.attributes.account_id);
					}
					if (App.doc_type == "INVRPT") {
						self.$el.find(".success-count span").html(successCount + " - " + data.attributes.product_name);
					}
				},
				error: function(jqXHR, textStatus, errorThrown) {
					errorCount += 1;
	                self.$el.find(".error-count span").html(errorCount);
					self.$el.find(".error-message").html(textStatus.responseText);
				}
			}).always(function() { 
				totalCount += 1;
				percentageComplete = (totalCount/totalDocuments) * 100
				self.$el.find(".progress-bar").css("width", percentageComplete + "%");
				self.$el.find(".info span").html(totalCount + " of " + totalDocuments);
				
				if (totalCount == totalDocuments) {
					self.$el.find(".btn-default").show();
				}
			});
        });
		*/
    },
	
	importDocument: function() {
		var found = false,
			self = this;
		
		_.each(App.selectedModels, function(document) {
			if (!found && document.attributes.flag == 0) {
				found = true;
				document.fetch({
			        data: $.param({"doc_type": App.doc_type, "doc_sys_no": document.attributes.doc_sys_no}),
					reset: true,
				    success: function(data) {
						self.successCount += 1;
						if (App.doc_type == "PARTIN") {
							self.$el.find(".success-count span").html(self.successCount + " - Rep: " + data.attributes.rep_id + "  Partner: " + data.attributes.account_id);
						}
						if (App.doc_type == "INVRPT") {
							self.$el.find(".success-count span").html(self.successCount + " - " + data.attributes.product_name);
						}
						
					},
					error: function(jqXHR, textStatus, errorThrown) {
						self.errorCount += 1;
		                self.$el.find(".error-count span").html(self.errorCount);
						var errorMessage = self.$el.find(".error-message").html();
						
						errorMessage += "<br>" + textStatus.responseText;
						self.$el.find(".error-message").html(errorMessage);
					}
				}).always(function() { 
					document.attributes.flag = 1;
					self.totalCount += 1;
					percentageComplete = (self.totalCount/self.totalDocuments) * 100
					self.$el.find(".progress-bar").css("width", percentageComplete + "%");
					self.$el.find(".info span").html(self.totalCount + " of " + self.totalDocuments);
				
					if (self.totalCount == self.totalDocuments) {
						self.$el.find(".btn-default").show();
					}
					self.importDocument();
				});
			}
        });
	}
});

App.View.FilterView = Backbone.View.extend({ 
	el: $(".filter-container"),
	
	events: {
		"click .btn-success": "filter",
		"change #doc_status": "showDateRange",
	},
	
    initialize: function() {

    },
    
    showDateRange: function () {
        if (this.$el.find("#doc_status").val() == "New") {
            this.$el.find(".filter-range").hide();
        } else {
            this.$el.find(".filter-range").show();
        }
    },
    
	filter: function () {
	    App.doc_type = this.$el.find("#doc_type").val();
	    App.doc_status = this.$el.find("#doc_status").val();
        App.View.documentView.render();
    },
});

App.View.DocumentView = Backbone.View.extend({ 
	el: $(".grid-container"),
	
	events: {
		"click #import_all": "importAll",
		"click #import_selected": "importSelected",
	},
	
    initialize: function() {
		this.initialLoad = true;
		this.$el.find("#import_all").hide();
		this.$el.find("#import_selected").hide();
		this.listenTo(App.Collection.documents, "reset", this.showState);
    },
    
    render: function () {
        showLoading();
		App.Collection.documents.reset();
        App.Collection.documents.state.currentPage = 1;
		App.Collection.documents.fetch({
			reset: true,
			data: $.param({
				type: App.doc_type, 
				status: App.doc_status, 
				start: App.rangeStart, 
				end: App.rangeEnd
				}),
		    success: function(data) {
				App.Grid.documentGrid = new Backgrid.Grid({
                    columns: App.Grid.eBridgeDocumentColumns,
                  	collection: App.Collection.documents,
                  	emptyText: "No documents found",
                });
                App.Grid.documentPaginator = new Backgrid.Extension.Paginator({
                  	collection: App.Collection.documents
                });
				$("#document_grid").html(App.Grid.documentGrid.render().$el);
				$("#document_paginator").html(App.Grid.documentPaginator.render().$el);
		   },
			error: function(jqXHR, textStatus, errorThrown) {
			    $("#document_info").html("Error getting documents");
				$("#document_grid").hide();
				$("#document_paginator").hide();
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
		    this.$el.find("#import_all").show();
    		this.$el.find("#import_selected").show();
			$("#document_info").html(from + "-" + to + " of " + response.state.totalRecords);
			$("#document_info").show();
			$("#document_grid").show();
			if (response.state.totalRecords > response.state.pageSize) {
				$("#document_paginator").show();
			} else {
				$("#document_paginator").hide();
			}
		} else {
		    this.$el.find("#import_all").hide();
    		this.$el.find("#import_selected").hide();
			$("#document_info").hide();
			if (this.initialLoad) {
				$("#document_filter").hide();
			}
			$("#document_paginator").hide();
		}
		
		this.initialLoad = false;
	},
	
	importAll: function() {
		App.selectedModels = App.Collection.documents.fullCollection.models;
		//App.selectedModels = App.Grid.documentGrid.fullCollection();
		App.View.import = new App.View.ImportView();
	},
	
	importSelected: function() {
		App.selectedModels = App.Grid.documentGrid.getSelectedModels();
		if (App.selectedModels.length > 0) {
		    App.View.import = new App.View.ImportView();
		}
	},
});

$(document).ready(function() {
	App.View.documentView = new App.View.DocumentView();
	App.View.filterView = new App.View.FilterView();
	
	App.rangeStart = moment().format("YYYY-MM-DD");
	App.rangeEnd = moment().format("YYYY-MM-DD");
	App.doc_type = "PARTIN";
    App.doc_status = "New";
	
	$('input[name="daterange"]').daterangepicker({ 
	      ranges: {
	         'Today': [moment(), moment()],
	         'Last 7 Days': [moment().subtract('days', 6), moment()],
	         'Last 30 Days': [moment().subtract('days', 29), moment()],
	      },
	      startDate: moment(),
	      endDate: moment(),
		  opens: "left"
	    },
	    function(start, end) {
	        App.rangeStart = start.format("YYYY-MM-DD");
        	App.rangeEnd = end.format("YYYY-MM-DD");
	    }
	);
});