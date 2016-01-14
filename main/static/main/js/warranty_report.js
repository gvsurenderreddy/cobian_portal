var App = {
	Model: {},
	Collection: {},
	View: {},
	Grid: {},
	report: "style",
	status: "ALL",
	dateRange: "ALL",
	startDate: moment().format('l'),
	endDate: moment().format('l'),
}

// ------------------------------------
//                REPORT
// ------------------------------------
App.View.ReportView = Backbone.View.extend({
    el: $("#report_view"),

    events: {
        "change select": "change",
    },

	initialize: function(){
		var report = getCookie("warrantyReport");
		if (report) {
			App.report = report;
		}
		this.$el.find("select").val(App.report);
	},

    show: function() {
        this.$el.show();
    },

    hide: function() {
        this.$el.hide();
    },

    change: function() {
        App.report = this.$el.find("select").val();
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
		var status = getCookie("warrantyReportStatus");
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
		var dateRange = getCookie("warrantyReportDateRange"),
			startDate = getCookie("warrantyReportStartDate"),
			endDate = getCookie("warrantyReportEndDate");

		if (dateRange) {
			App.dateRange = dateRange;
			App.startDate = startDate;
			App.endDate = endDate;
		}
		this.$el.find("select").val(App.dateRange);
        $('#daterange').val(App.startDate + ' - ' + App.endDate);

        $('#daterange').daterangepicker({
            timePicker: false,
            format: 'YYYY-MM-DD',
            ranges: {
                     'Today': [moment(), moment()],
                     'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                     'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                     'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                     'Last 60 Days': [moment().subtract(59, 'days'), moment()],
                     'Last 90 Days': [moment().subtract(89, 'days'), moment()],
                     'This Month': [moment().startOf('month'), moment().endOf('month')],
                     'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
                     'This Year': [moment().startOf('year'), moment().endOf('year')],
                     'Last Year': [moment().subtract(1, 'year').startOf('year'), moment().subtract(1, 'year').endOf('year')]
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
        setCookie("warrantyReport", App.report, 30);
		setCookie("warrantyReportStatus", App.status, 30);
		setCookie("warrantyReportDateRange", App.dateRange, 30);
        setCookie("warrantyReportStartDate", App.startDate, 30);
        setCookie("warrantyReportEndDate", App.endDate, 30);

        App.View.gridView.render();
    }
});


// ------------------------------------
//               REPORT
// ------------------------------------
App.Grid.styleColumns = [{name: "id", label: "", cell: "string"},
                         {name: "style", label: "STYLE", cell: "string"},
                         {name: "count", label: "COUNT", cell: "string"}];

App.Grid.styleColorColumns = [{name: "id", label: "", cell: "string"},
                              {name: "style", label: "STYLE", cell: "string"},
                              {name: "color", label: "COLOR", cell: "string"},
                              {name: "count", label: "COUNT", cell: "string"}];

App.Grid.styleDamageColumns = [{name: "id", label: "", cell: "string"},
                               {name: "style", label: "STYLE", cell: "string"},
                               {name: "damage", label: "DAMAGE", cell: "string"},
                               {name: "count", label: "COUNT", cell: "string"}];

App.Grid.styleColorDamageColumns = [{name: "id", label: "", cell: "string"},
                                    {name: "style", label: "STYLE", cell: "string"},
                                    {name: "color", label: "COLOR", cell: "string"},
                                    {name: "damage", label: "DAMAGE", cell: "string"},
                                    {name: "count", label: "COUNT", cell: "string"}];

App.Grid.damageColumns = [{name: "id", label: "", cell: "string"},
                          {name: "damage", label: "DAMAGE", cell: "string"},
                          {name: "count", label: "COUNT", cell: "string"}];

App.Grid.damageStyleColumns = [{name: "id", label: "", cell: "string"},
                               {name: "damage", label: "DAMAGE", cell: "string"},
                               {name: "style", label: "STYLE", cell: "string"},
                               {name: "count", label: "COUNT", cell: "string"}];

App.Grid.damageColorColumns = [{name: "id", label: "", cell: "string"},
                               {name: "damage", label: "DAMAGE", cell: "string"},
                               {name: "color", label: "COLOR", cell: "string"},
                               {name: "count", label: "COUNT", cell: "string"}];

App.Grid.damageStyleColorColumns = [{name: "id", label: "", cell: "string"},
                                    {name: "style", label: "STYLE", cell: "string"},
                                    {name: "damage", label: "DAMAGE", cell: "string"},
                                    {name: "color", label: "COLOR", cell: "string"},
                                    {name: "count", label: "COUNT", cell: "string"}];

App.Model.Report = Backbone.Model.extend({});
App.Collection.Report = Backbone.Collection.extend({
	model: App.Model.Report,
	mode: "client",
	url: "/api/report/warranty/",
});
App.Collection.report = new App.Collection.Report();

App.View.GraphView = Backbone.View.extend({
    el: $("#graph_container"),

    renderSingle: function (data) {
        this.$el.html("");

        /*var data = [
            {key: "A", value: 10},
            {key: "B", value: 20},
            {key: "C", value: 30},
            {key: "D", value: 40},
            {key: "E", value: 50},
        ]*/

        var margin = {top: 20, right: 10, bottom: 20, left: 30},
            width = this.$el.width() - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(10);

        var svg = d3.select("#graph_container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        x.domain(data.map(function(d) { return d.key; }));
        y.domain([0, d3.max(data, function(d) { return d.value; })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end");

        svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.key); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); });
    },

    renderGroup: function (rawData) {
        this.$el.html("");

        /*var rawData = [
            {group: "Style 1", key: "Rip", value: 10},
            {group: "Style 1", key: "Tear", value: 20},
            {group: "Style 2", key: "Pop", value: 30},
            {group: "Style 3", key: "Rip", value: 40},
            {group: "Style 3", key: "Broke", value: 50},
        ]*/

        var dataDict = {},
            groups = [],
            keyDict = {},
            keys = [];

        _.each(rawData, function(dataItem) {
            if (!keyDict[dataItem.key]) {
                keys.push(dataItem.key);
                keyDict[dataItem.key] = 1;
            }
            if (!dataDict[dataItem.group]) {
                groups.push(dataItem.group);
                dataDict[dataItem.group] = [];
            }
            dataDict[dataItem.group].push({
                key: dataItem.key,
                value: dataItem.value
            })
        });

        var data = [];
        _.each(dataDict, function(keyArray, key) {
            data.push({group: key, keys: keyArray})
        });

        var margin = {top: 20, right: 10, bottom: 20, left: 30},
            width = this.$el.width() - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var x0 = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);

        var x1 = d3.scale.ordinal();

        var y = d3.scale.linear()
            .range([height, 0]);

        var color = d3.scale.ordinal()
            .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00",
                    "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9",
                    "#bc80bd", "#ccebc5", "#ffed6f"]);

        var xAxis = d3.svg.axis()
            .scale(x0)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .ticks(10);

        var svg = d3.select("#graph_container").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        x0.domain(data.map(function(d) { return d.group; }));
        x1.domain(keys).rangeRoundBands([0, x0.rangeBand()]);
        y.domain([0, d3.max(data, function(d) { return d3.max(d.keys, function(d) { return d.value; }); })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

         svg.append("g")
              .attr("class", "y axis")
              .call(yAxis)
            .append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em");

          var group = svg.selectAll(".group")
              .data(data)
            .enter().append("g")
              .attr("class", "group")
              .attr("transform", function(d) { return "translate(" + x0(d.group) + ",0)"; });

          group.selectAll("rect")
              .data(function(d) { return d.keys; })
            .enter().append("rect")
              .attr("width", x1.rangeBand())
              .attr("x", function(d) { return x1(d.key); })
              .attr("y", function(d) { return y(d.value); })
              .attr("height", function(d) { return height - y(d.value); })
              .style("fill", function(d) { return color(d.key); });

          var legend = svg.selectAll(".legend")
              .data(keys.slice().reverse())
            .enter().append("g")
              .attr("class", "legend")
              .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

          legend.append("rect")
              .attr("x", width - 18)
              .attr("width", 18)
              .attr("height", 18)
              .style("fill", color);

          legend.append("text")
              .attr("x", width - 24)
              .attr("y", 9)
              .attr("dy", ".35em")
              .style("text-anchor", "end")
              .text(function(d) { return d; });
    },
});

App.View.GridView = Backbone.View.extend({
    el: $("#grid_container"),

    render: function () {
        App.View.dateView.setDates();

        var self = this;
        showLoading();

        this.$('#grid_helper').html('Loading...');

        var columns = App.Grid.styleColumns;
        switch (App.report) {
            case "style-color":
                columns = App.Grid.styleColorColumns;
                break;
            case "style-damage":
                columns = App.Grid.styleDamageColumns;
                break;
            case "style-color-damage":
                columns = App.Grid.styleColorDamageColumns;
                break;
            case "damage":
                columns = App.Grid.damageColumns;
                break;
            case "damage-style":
                columns = App.Grid.damageStyleColumns;
                break;
            case "damage-color":
                columns = App.Grid.damageColorColumns;
                break;
            case "damage-style-color":
                columns = App.Grid.damageStyleColorColumns;
                break;
        }

        App.Grid.grid = new Backgrid.Grid({
          	columns: columns,
          	collection: App.Collection.report,
          	emptyText: "No data found",
        });

        App.Grid.filter = new simpleFilter({
          collection: App.Collection.report,
          placeholder: "Search",
          fields: ["count", "damage", "style", "color"],
        });

		App.Collection.report.fetch({
			reset: true,
			data: $.param({
			    "report": App.report,
				"status": App.status,
				"date_range": App.dateRange,
				"start_date": App.startDate,
				"end_date": App.endDate
			}),
		    success: function(data) {
		        // Create graph data
		        var graphData = [],
		            graphType = "group";
		        App.Collection.report.each(function(data) {
		            switch (App.report) {
                        case "style":
                            graphType = "single";
                            graphData.push({key: data.attributes.style, value: data.attributes.count});
                            break;
                        case "style-color":
                            graphData.push({
                                group: data.attributes.style,
                                key: data.attributes.color,
                                value: data.attributes.count});
                            break;
                        case "style-damage":
                            graphData.push({
                                group: data.attributes.style,
                                key: data.attributes.damage,
                                value: data.attributes.count});
                            break;
                        case "damage":
                            graphType = "single";
                            graphData.push({key: data.attributes.damage, value: data.attributes.count});
                            break;
                        case "damage-style":
                            graphData.push({
                                group: data.attributes.style,
                                key: data.attributes.damage,
                                value: data.attributes.count});
                            break;
                        case "damage-color":
                            graphData.push({
                                group: data.attributes.color,
                                key: data.attributes.damage,
                                value: data.attributes.count});
                            break;
                    }
				});

				self.$('#grid_helper').empty();
				self.$("#grid_filter").html(App.Grid.filter.render().el);
                self.$("#grid").html(App.Grid.grid.render().$el);

                if (graphType == "single") {
                    App.View.graphView.renderSingle(graphData);
                } else {
                    App.View.graphView.renderGroup(graphData);
                }

			},
			error: function(jqXHR, textStatus, errorThrown) {
 				self.$('#grid_helper').html('Error loading report');
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
    App.View.reportView = new App.View.ReportView();
    App.View.statusView = new App.View.StatusView();
    App.View.dateView = new App.View.DateView();
    App.View.buttonView = new App.View.ButtonView();
    App.View.graphView = new App.View.GraphView();
    App.View.gridView = new App.View.GridView();

    App.View.gridView.render();
});
