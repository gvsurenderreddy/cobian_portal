// ------------------------------------
//                STATUS
// ------------------------------------
App.View.StatusView = Backbone.View.extend({
    el: $("#status_view"),

    events: {
        "change select": "change",
    },

    initialize: function() {
        var html = ""

        if (App.userAuthorizer) {
            html += '<option value="ALL">All Status</option>';
            html += '<option value="NEW">New</option>';
            html += '<option value="PREAUTHORIZED">Pre-Authorized</option>';
            html += '<option value="RECEIVED">Received</option>';
            html += '<option value="AUTHORIZED">Authorized</option>';
            html += '<option value="NOTAUTHORIZED">Not Authorized</option>';
            html += '<option value="CLOSED">Closed</option>';

            var status = getCookie("warrantyStatus");
            if (status) {
                App.status = status;
            }
        } else if (App.userReceiver) {
            html += '<option value="PREAUTHORIZED">Pre-Authorized</option>';
            App.status = "PREAUTHORIZED";
        } else {
            html = '<option value="NEW">New</option>';
            App.status = "NEW";
        }
        this.$el.find("select").html(html);
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
		setCookie("warrantyStatus", App.status, 30);
		setCookie("warrantyDateRange", App.dateRange, 30);
        setCookie("warrantyStartDate", App.startDate, 30);
        setCookie("warrantyEndDate", App.endDate, 30);

        App.View.gridView.render();
    }
});


// ------------------------------------
//            CLAIMS
// ------------------------------------
App.Grid.columns = [
	{
		name: "claimNumber",
		label: "CLAIM #",
		editable: false,
		sortType: "toggle",
		direction: "ascending",
		cell: Backgrid.StringCell.extend({
			render: function () {
				var html = '<a href="/warranty/' + this.model.attributes.id + '/">' + this.model.attributes.claimNumber + '</a>';
				this.$el.empty();
				this.$el.html(html);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "name",
		label: "NAME",
		editable: false,
		sortType: "toggle",
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.name);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "style",
		label: "STYLE",
		editable: false,
		sortType: "toggle",
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.style);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "color",
		label: "COLOR",
		editable: false,
		sortType: "toggle",
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.color);
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
				this.$el.html(this.model.attributes.statusDescription);
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
				this.$el.html(unixTimeToString(this.model.attributes.statusDate, false));
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
			    this.$el.empty();
                this.$el.html('<div class="btn btn-danger btn-xs delete">Remove</div>');
                this.delegateEvents();
				return this;
			}
		})
	},
];

App.Grid.row = Backgrid.Row.extend({
    events: {
        "click .delete": "delete",
    },
    delete: function () {
        Backbone.trigger("deleteClicked", this.model);
    },
});
Backbone.on("deleteClicked", function (model) {
    App.View.removeView.show(model);
});

App.Model.Warranty = Backbone.Model.extend({});
App.Collection.Warranties = Backbone.ShowMoreCollection.extend({
	model: App.Model.Warranty,
	mode: "client",
	url: "/api/warranties/",
	state: {
		pageSize: 25,
	},
});
App.Collection.warranties = new App.Collection.Warranties();

App.View.GridView = Backbone.View.extend({
    el: $("#grid_container"),

    render: function () {
        App.View.dateView.setDates();

        var self = this;
        showLoading();

        this.$('#grid_helper').html('Loading...');

        App.Grid.grid = new Backgrid.Grid({
          	columns: App.Grid.columns,
          	row: App.Grid.row,
          	collection: App.Collection.warranties,
          	emptyText: "No claims found",
          	footer: Backgrid.ShowMoreFooter
        });

        App.Grid.filter = new simpleFilter({
          collection: App.Collection.warranties,
          placeholder: "Search",
          fields: ["claimNumber", "name", "style", "color"],
        });

        App.Collection.warranties.state.pageSize = 25;
        App.Collection.warranties.state.currentPage = 1;
		App.Collection.warranties.fetch({
			reset: true,
			data: $.param({
				"status": App.status,
				"date_range": App.dateRange,
				"start_date": App.startDate,
				"end_date": App.endDate
			}),
		    success: function(data) {
				self.$('#grid_helper').empty();
				self.$("#grid_filter").html(App.Grid.filter.render().el);
                self.$("#grid").html(App.Grid.grid.render().$el);
			    //self.$('#grid_helper').html(accounting.formatMoney(App.total));
			},
			error: function(jqXHR, textStatus, errorThrown) {
 				self.$('#grid_helper').html('Error loading claims');
			}
		}).always(function() {
		    self.show();
		    self.displayDeleteColumn();
            hideLoading();
		});
    },

    displayDeleteColumn: function() {
        if ((App.status == "NEW" || App.status == "PREAUTHORIZED") && App.userAuthorizer) {
            if ($("#grid").hasClass("nodelete")) {
                $("#grid").removeClass("nodelete");
            }
        } else {
            if (!$("#grid").hasClass("nodelete")) {
                $("#grid").addClass("nodelete");
            }
        }
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
//            REMOVE CLAIM
// ------------------------------------
App.View.RemoveView = Backbone.View.extend({
    el: $("#remove_modal"),

    events: {
        "click .btn-danger": "click",
    },

    show: function(model) {
        this.model = model;
        this.$el.find(".modal-body").html('<p>Are you sure you want to delete ' + model.attributes.claimNumber + '?</p>');
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
    App.View.statusView = new App.View.StatusView();
    App.View.dateView = new App.View.DateView();
    App.View.buttonView = new App.View.ButtonView();
    App.View.removeView = new App.View.RemoveView();
    App.View.gridView = new App.View.GridView();

    App.View.gridView.render();
});
