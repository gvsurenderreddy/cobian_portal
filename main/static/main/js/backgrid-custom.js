/*
	Custom things for backgrid
*/

//custom backgrid filter that avoids using a <form>
var simpleFilter = Backgrid.Extension.ClientSideFilter.extend({
    events: _.extend({}, Backgrid.Extension.ClientSideFilter.prototype.events, {
      "keyup input[type=text]": "search",
    }),
	tagName: 'div',
	className: 'input-group input-group-sm filter',
	template: _.template('<span class="input-group-addon"><span class="glyphicon glyphicon-search"></span></span><input type="search" class="form-control filter-input" <% if (placeholder) { %> placeholder="<%- placeholder %>" <% } %>>'),
	wait: 150
});

var simpleServerSideFilter = Backgrid.Extension.ServerSideFilter.extend({
    events: _.extend({}, Backgrid.Extension.ServerSideFilter.prototype.events, {
      "keyup input[type=search]": "search",
    }),
	initialize: function() {
		simpleServerSideFilter.__super__.initialize.apply(this, arguments);
		this.search = _.debounce(this.search, this.wait); //applies wait to search keyup
	},
	tagName: 'div',
	className: 'input-group input-group-sm filter',
	template: _.template('<span class="input-group-addon"><span class="glyphicon glyphicon-search"></span></span><input type="search" class="form-control filter-input" <% if (placeholder) { %> placeholder="<%- placeholder %>" <% } %>>'),
	wait: 300
});




/*
var simpleSelectFilter = Backgrid.Extension.SelectFilter.extend({
    tagName: "label",
    className: "custom-select",
    template: _.template([
      "<select>",
      "<% for (var i=0; i < options.length; i++) { %>",
      "  <option value='<%=JSON.stringify(options[i].value)%>' <%=options[i].value === initialValue ? 'selected=\"selected\"' : ''%>><%=options[i].label%></option>",
      "<% } %>",
      "</select>"
    ].join("\n")),  
    events: {
      "change select": "onChange"
    },    
    currentValue: function() {
      return JSON.parse(this.$el.find('select').val());
    },    
});
*/

/*
  showMore() Adds more models to the first page of a pageable collection.
  It does this by resetting the collection to the current collection plus a number of models
  from fullCollection, and increases the page size to the number of currently-visible models.
*/
Backbone.ShowMoreCollection = Backbone.PageableCollection.extend({
  initialize: function() {
    Backbone.PageableCollection.prototype.initialize.apply(this, arguments);
    this.originalPageSize = this.state.pageSize;
    var self = this;
    this.on("reset", function() {
      self.pageSize = self.originalPageSize;
    });
  },
  showMore: function(num) { 
    var num = num || 10;
    var state = this.state;
    var pageNum = state.currentPage;
    var pageSize = state.pageSize + num;
    this.state = this._checkState(_.extend({}, state, {currentPage: pageNum, pageSize:pageSize}));


    var last = this.fullCollection.indexOf(this.last());
    var nextSlice = this.fullCollection.slice(last, last+num);
    var currentModels = this.models;

    var comparator = this.comparator;
    this.comparator = null;
    this.reset(_.union(currentModels, nextSlice));

    this.comparator = comparator;
    if (comparator) this.sort();    

    // return true if there are more to show
    return this.length < this.fullCollection.length;
  }
});

Backgrid.ShowMoreFooter = Backgrid.Footer.extend({
  events: {
    'click .show-more' : 'getMore'
  },
  template: _.template('<tr><td class="renderable" colspan="40"></td></tr>'),
  initialize: function() {
    Backgrid.Footer.prototype.initialize.apply(this, arguments);
    this.listenTo(this.collection, "reset", this.render);
  },
  render: function() {
    this.$el.html(this.template());
    var currentPage = this.collection.state.currentPage
    var pageSize = this.collection.state.pageSize;
    var originalPageSize = this.collection.originalPageSize
    var total = this.collection.state.totalRecords;
    if (total-pageSize < originalPageSize) {
      originalPageSize = total-pageSize;
    }
    var content = this.checkShowMoreButton() ?
      '<div class="btn btn-link show-more" style="width:100%;padding:0;font-size:12px">Show '+originalPageSize+' more ('+total+' total)</div>' : '<div style="width:100%;text-align:center">Showing all '+this.collection.length + '</div>'
    if (this.collection.length == 0) {
      content = ''
    }
    this.$('td').html(content);
    this.delegateEvents();
    return this;
  },
  getMore: function() {
      var originalPageSize = this.collection.originalPageSize
      this.collection.showMore(originalPageSize);
  },
  checkShowMoreButton: function() {
    return this.collection.length < this.collection.fullCollection.length
  }
});

Backgrid.ShowMoreFooterServer = Backgrid.Footer.extend({
  events: {
    'click .show-more' : 'getMore'
  },
  template: _.template('<tr><td class="renderable" colspan="40"></td></tr>'),
  initialize: function() {
    Backgrid.Footer.prototype.initialize.apply(this, arguments);
    this.listenTo(this.collection.pageableCollection, "sync", this.render);
  },
  render: function() {
    var self = this;
    
    var collection = this.collection.pageableCollection;
    
    this.$el.html(this.template());
    var currentPage = collection.state.currentPage
    var currentSize = this.collection.length
    var pageSize = collection.state.pageSize;
    var total = collection.state.actualTotal;
    if (total-currentSize < pageSize) {
      pageSize = total-currentSize;
    }
    var content = this.checkShowMoreButton() ?
      '<div class="btn btn-link show-more" style="width:100%;padding:0;font-size:12px">Show '+pageSize+' more ('+total+' total)</div>' :
      '<div style="width:100%;text-align:center">Showing all '+total + '</div>'
    if (collection.length == 0) {
      content = ''
    }
    this.$('td').html(content);
    this.delegateEvents();
    return this;
  },
  getMore: function() {
    this.collection.pageableCollection.getNextPage();
  },
  checkShowMoreButton: function() {
    return this.collection.length < this.collection.pageableCollection.state.actualTotal;
  }  
});

/*
Adds server-side sorting to header cells for infinite server-side grid.
Must have sortType: 'toggle'
*/
Backgrid.SortableServerSideHeaderCell = Backgrid.HeaderCell.extend({
    /* direction() is same as original */
    direction: function (dir) {
      if (arguments.length) {
        var direction = this.column.get('direction');
        if (direction) this.$el.removeClass(direction);
        if (dir) this.$el.addClass(dir);
        this.column.set('direction', dir)
      }
      return this.column.get('direction');
    },
    onClick: function (e) {
      e.preventDefault();

      var collection = this.collection, event = "backgrid:sort";

      function cycleSort(header, col) {
        if (header.direction() === "ascending") collection.trigger(event, col, "descending");
        else if (header.direction() === "descending") collection.trigger(event, col, null);
        else collection.trigger(event, col, "ascending");
      }

      function toggleSort(header, col) {
        var direction = header.direction() === "ascending" ? "descending" : "ascending";
        var dir_id = header.direction() === "ascending" ? -1 : 1;
        var sort_by = col.get('name');
        collection.pageableCollection.setSorting(sort_by, dir_id);
        collection.pageableCollection.fetch({
          wait:true,
          success: function() {
            collection.trigger(event, col, direction);
          }
        });
      }

      var column = this.column;
      var sortable = Backgrid.callByNeed(column.sortable(), column, this.collection);
      if (sortable) {
        var sortType = column.get("sortType");
        if (sortType === "toggle") toggleSort(this, column);
        else cycleSort(this, column);
      }
    },      
    })