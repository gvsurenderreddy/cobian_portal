App.Model.Warranty = Backbone.Model.extend({
	url: "/api/warranty/" + App.warrantyId + "/",
});
App.Model.warranty = new App.Model.Warranty();


// ------------------------------------
//               FORM
// ------------------------------------
App.Model.WarrantyDefect = Backbone.Model.extend({});
App.Collection.WarrantyDefects = Backbone.Collection.extend({
	model: App.Model.WarrantyDefect,
	mode: "client",
	url: "/api/warranty/defects/",
});
App.Collection.warrantyDefects = new App.Collection.WarrantyDefects();

App.View.FormView = Backbone.View.extend({
    el: $("#form_view"),

    events: {
        "change input": "inputChange",
        "change select": "inputChange",
        "click .style": "selectStyle",
        "click .color": "selectColor",
    },

	initialize: function() {
	    App.statuses = {
	        "NEW": "New Claim",
            "PREAUTHORIZED": "Pre-Authorized",
            "RECEIVED": "Received",
            "AUTHORIZED": "Authorized",
            "NOTAUTHORIZED": "Not Authorized",
            "CLOSED": "Closed"
        }

        this.loadDefects();
	},

    show: function() {
        if (!$("#form_body").hasClass("in")) {
            $("#form_body").collapse('toggle');
        }
    },

    selectStyle: function() {
        App.View.styleColorView.renderStyles();
    },

    selectColor: function() {
        App.View.styleColorView.renderColors();
    },

	render: function() {
	    var self = this;

		showLoading();

		App.Model.warranty.fetch({
			reset: true,
		    success: function(data) {
		        self.$el.find(".panel-title a").html("CLAIM #" + data.attributes.claimNumber);
                self.$el.find(".status").html(data.attributes.statusDescription + " - " + unixTimeToString(data.attributes.statusDate, false));

                App.status = data.attributes.status;

                $("#breadcrumb_claim").html(data.attributes.claimNumber);
                $("#name").val(data.attributes.name);
                $("#email").val(data.attributes.email);
                $("#phone").val(data.attributes.phone);
                $("#address").val(data.attributes.address);
                $("#style").val(data.attributes.style);
                $("#color").val(data.attributes.color);
                $("#damage").val(data.attributes.damage);
                $("#notes").val(data.attributes.notes);

                if (data.attributes.imageOverride) {
                    $("#image_override").attr("checked", "checked");
                }

                App.View.buttonView.setStatusButton(data.attributes.status);
            },
			error: function(jqXHR, textStatus, errorThrown) {
				alert(textStatus.responseText);
			}
        }).always(function() {
            hideLoading();
        });
	},

    loadDefects: function() {
        var self = this;

		App.Collection.warrantyDefects.fetch({
			reset: true,
		    success: function(data) {
		        var html = ""
                App.Collection.warrantyDefects.each(function(defect) {
                    html += '<option value="' + defect.attributes.description + '">' + defect.attributes.description + '</option>';
                });
                $("#damage").html(html);
			},
			error: function(jqXHR, textStatus, errorThrown) {
			    var tmp = testStatus;
			}
		}).always(function() {
		});
    },

    inputChange: function() {
		App.View.buttonView.enableSave(true);
	},
});

// ------------------------------------
//             STYLES/COLOR
// ------------------------------------
App.Model.WarrantyColor = Backbone.Model.extend({});
App.Collection.WarrantyColors = Backbone.Collection.extend({
	model: App.Model.WarrantyColor,
	mode: "client",
	url: "/api/warranty/colors/",
});
App.Collection.warrantyColors = new App.Collection.WarrantyColors();

App.Model.WarrantyStyle = Backbone.Model.extend({});
App.Collection.WarrantyStyles = Backbone.Collection.extend({
	model: App.Model.WarrantyStyle,
	mode: "client",
	url: "/api/warranty/styles/",
});
App.Collection.warrantyStyles = new App.Collection.WarrantyStyles();

App.View.StyleColorView = Backbone.View.extend({
    el: $("#style_color_modal"),

    events: {
        "click .btn-success": "select",
    },

    initialize: function () {
        this.loadColors();
    },

    loadColors: function () {
        var self = this;

		App.Collection.warrantyColors.fetch({
			reset: true,
		    success: function(data) {
		        var tmp = data;
			},
			error: function(jqXHR, textStatus, errorThrown) {
			}
		}).always(function() {
		    self.loadStyles()
		});
    },

    loadStyles: function () {
        var self = this;

		App.Collection.warrantyStyles.fetch({
			reset: true,
		    success: function(data) {
		        var tmp = data;
			},
			error: function(jqXHR, textStatus, errorThrown) {
			    var tmp = testStatus;
			}
		}).always(function() {
		    self.loadDefects()
		});
    },

    loadDefects: function () {
        var self = this;

		App.Collection.warrantyDefects.fetch({
			reset: true,
		    success: function(data) {
		        var tmp = data;
			},
			error: function(jqXHR, textStatus, errorThrown) {
			    var tmp = testStatus;
			}
		}).always(function() {
		});
    },

    renderColors: function() {
        this.selectMode = "COLOR";
        this.$el.find(".modal-title").html("Select Color");
        var currentColor = $("#color").val();

        var html = ""
        App.Collection.warrantyColors.each(function(color) {
	        var selected = "";
            if (color.attributes.color.toLowerCase() == currentColor.toLowerCase()) {
                selected = "selected";
            }
	        html += '<option value="' + color.attributes.color + '" ' + selected + '>' + color.attributes.color + '</option>';
	    });
	    this.$el.find("select").html(html);
	    this.show();
    },

    renderStyles: function() {
        this.selectMode = "STYLE";
        this.$el.find(".modal-title").html("Select Style");
        var currentStyle = $("#style").val();

        var html = ""
        App.Collection.warrantyStyles.each(function(style) {
            var selected = "";
            if (style.attributes.style.toLowerCase() == currentStyle.toLowerCase()) {
                selected = "selected";
            }
	        html += '<option value="' + style.attributes.style + '" ' + selected + '>' + style.attributes.style + '</option>';
	    });
	    this.$el.find("select").html(html);
	    this.show();
    },

    renderDefects: function() {
        this.selectMode = "DEFECT";
        this.$el.find(".modal-title").html("Select Damage/Defect");
        var currentDefect = $("#damage").val();

        var html = ""
        App.Collection.warrantyDefects.each(function(defect) {
            var selected = "";
            if (defect.attributes.description.toLowerCase() == currentDefect.toLowerCase()) {
                selected = "selected";
            }
	        html += '<option value="' + defect.attributes.description + '" ' + selected + '>' + defect.attributes.description + '</option>';
	    });
	    this.$el.find("select").html(html);
	    this.show();
    },

	select: function() {
	    var selectValue = this.$el.find("select").val();
        if (this.selectMode == "STYLE") {
            $("#style").val(selectValue);
        } else if (this.selectMode == "COLOR") {
            $("#color").val(selectValue);
        } else {
            $("#damage").val(selectValue);
        }
        this.hide();
        App.View.buttonView.enableSave(true);
	},

	show: function() {
	    this.$el.modal('show');
	},

	hide: function() {
	    this.$el.modal('hide');
	},
});


// ------------------------------------
//               NOTES
// ------------------------------------
App.View.NotesView = Backbone.View.extend({
    el: $("#notes_view"),

    events: {
        "change textarea": "change",
        "click .btn-primary": "timeStamp"
    },

	change: function(event) {
		App.View.buttonView.enableSave(true);
	},

	timeStamp: function() {
	    var currentValue = this.$el.find("textarea").val(),
	        dateNow = new Date();

	    currentValue += dateNow + " by " + App.userName + ": ";
	    this.$el.find("textarea").val(currentValue);
	    App.View.buttonView.enableSave(true);
	}
});

// ------------------------------------
//               IMAGES
// ------------------------------------
App.Grid.columns = [
	{
		name: "type",
		label: "TYPE",
		editable: false,
		sortType: "toggle",
		direction: "ascending",
		cell: Backgrid.StringCell.extend({
			render: function () {
			    var imageType = {
			        "IMAGE": "Product Image",
			        "PROOF": "Proof of Purchase"
			    }
				this.$el.empty();
				this.$el.html(imageType[this.model.attributes.type]);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "filePath",
		label: "IMAGE",
		editable: false,
		sortType: "toggle",
		cell: Backgrid.StringCell.extend({
			render: function () {
			    var html = '<a href="' + this.model.attributes.filePath + '" target="_blank"><img src="' + this.model.attributes.filePath + '" width="180" class="img-responsive" /></a>'
				this.$el.empty();
				this.$el.html(html);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "description",
		label: "DESCRIPTION",
		editable: false,
		sortType: "toggle",
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.description);
				this.delegateEvents();
				return this;
			}
		})
	},
	{
		name: "uploaded",
		label: "UPLOAD DATE",
		editable: false,
		sortType: "toggle",
		cell: Backgrid.StringCell.extend({
			render: function () {
				this.$el.empty();
				this.$el.html(this.model.attributes.uploadDate);
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
			    var html = '<div class="btn btn-danger btn-sm delete">Remove</div>';

                this.$el.empty();
				this.$el.html(html);
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


App.Model.Image = Backbone.Model.extend({});
App.Collection.Images = Backbone.Collection.extend({
	model: App.Model.Image,
	mode: "client",
	url: function() {
	    return "/api/warranty/" + App.warrantyId + "/images/";
	    },
});
App.Collection.images = new App.Collection.Images();

App.View.ImagesView = Backbone.View.extend({
    el: $("#images_view"),

    events: {
        "click .upload": "upload",
    },

    render: function () {
        var self = this;

        App.Grid.grid = new Backgrid.Grid({
          	columns: App.Grid.columns,
          	collection: App.Collection.images,
          	row: App.Grid.row,
          	emptyText: "No images found",
        });

		App.Collection.images.fetch({
			reset: true,
		    success: function(data) {
                self.$("#grid").html(App.Grid.grid.render().$el);
			},
			error: function(jqXHR, textStatus, errorThrown) {
 				self.$('#grid_helper').html('Error loading images');
			}
		}).always(function() {
		});
    },

    show: function() {
        if (!$("#images_body").hasClass("in")) {
            $("#images_body").collapse('toggle');
        }
    },

	upload: function(event) {
        App.View.uploadView.show();
	},

	enableUpload: function(enabled) {
		this.$el.find(".upload").attr("disabled", !enabled);
	},
});

// ------------------------------------
//            REMOVE IMAGE
// ------------------------------------
App.View.RemoveView = Backbone.View.extend({
    el: $("#remove_image_modal"),

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
				App.View.imagesView.render();
				self.$el.modal('hide');
			},
			error: function(jqXHR, textStatus, errorThrown) {
                self.$el.modal('hide');
			}
		});
    }
});

// ------------------------------------
//               UPLOAD
// ------------------------------------
App.View.UploadView = Backbone.View.extend({
    el: $("#upload_modal"),

    events: {
        "click .btn-success": "success",
    },

	success: function() {
	    if (this.validate()) {
	        $("#file_upload_form").submit();
	    }

	},

    validate: function() {
        var description = this.$el.find("#image_description").val(),
            input_file = this.$el.find("#input_file").val();

        this.$el.find(".help-block").html("");

        if (description.length == 0) {
            this.$el.find(".help-block.description").html("Please add a description for this image");
            return false;
        }

        if (input_file.length == 0) {
            this.$el.find(".help-block.file").html("Please select an image to upload");
            return false;
        }

        return true;
    },

	show: function() {
	    this.$el.find(".help-block").html("");
	    this.$el.modal("show");
	},

	hide: function() {
	    this.$el.modal("hide");
	}
});

// ------------------------------------
//               HISTORY
// ------------------------------------
App.Model.History = Backbone.Model.extend({});
App.Collection.History = Backbone.Collection.extend({
	model: App.Model.History,
	mode: "client",
	url: function() {
	    return "/api/warranty/" + App.warrantyId + "/history/";
	    },
});
App.Collection.history = new App.Collection.History();

App.View.HistoryView = Backbone.View.extend({
    el: $("#history_view"),

    initialize: function() {
        var self = this;

        App.Collection.history.fetch({
			reset: true,
		    success: function(data) {
		        html = ""
			    App.Collection.history.each(function(history) {
					html += '<p>' + unixTimeToString(history.attributes.actionDate, true) + ' - ' + history.attributes.action + " by " + history.attributes.user + '<p>';
				});
				self.$el.find(".panel-body").html(html);
			},
			error: function(jqXHR, textStatus, errorThrown) {
			}
		}).always(function() {
		});
    },

});

// ------------------------------------
//             BUTTON VIEW
// ------------------------------------
App.View.ButtonView = Backbone.View.extend({
    el: $("#button_view"),

    events: {
		"click #button_save": "buttonSave",
		"click #button_pre_authorized": "buttonPreAuthorized",
		"click #button_received": "buttonReceived",
		"click #button_authorized": "buttonAuthorized",
		"click #button_not_authorized": "buttonNotAuthorized",
		"click #button_closed": "buttonClosed",
    },

    setStatusButton: function(status) {
        switch (status) {
            case "NEW":
                $("#button_pre_authorized").show();
                break;

            case "PREAUTHORIZED":
                $("#button_received").show();
                break;

            case "RECEIVED":
                $("#button_authorized").show();
                $("#button_not_authorized").show();
                break;

            case "AUTHORIZED":
                $("#button_closed").show();
                break;

            case "NOTAUTHORIZED":
                $("#button_authorized").show();
                break;

            case "CLOSED":
                this.$el.find("#button_save").hide();
                break;
        }
    },

	enableSave: function(enabled) {
		this.$el.find("#button_save").attr("disabled", !enabled);
		App.View.imagesView.enableUpload(!enabled);
	},

    validate: function() {
        var name = $("#name").val(),
            email = $("#email").val(),
		    phone = $("#phone").val(),
		    address = $("#address").val(),
		    style = $("#style").val(),
		    color = $("#color").val(),
		    damage = $("#damage").val(),
		    errorMessage = "";

        App.errorView = "FORM";

		if (name.length == 0) {
		    App.errorView = "FORM";
		    $(".error-message").html("Please enter a name");
            $(".help-block.name").html("Please enter a name");
            return false;
        }

        if (email.length == 0) {
            $(".error-message").html("Please enter an email address");
            $(".help-block.email").html("Please enter an email address");
            return false;
        }

        if (phone.length == 0) {
            $(".error-message").html("Please enter a phone number");
            $(".help-block.phone").html("Please enter a phone number");
            return false;
        }

        if (address.length == 0) {
            $(".error-message").html("Please enter an address");
            $(".help-block.address").html("Please enter an address");
            return false;
        }

        if (style.length == 0) {
            $(".error-message").html("Please select a style");
            $(".help-block.style").html("Please select a style");
            return false;
        }

        if (color.length == 0) {
            $(".error-message").html("Please select a color");
            $(".help-block.color").html("Please select a color");
            return false;
        }

        if (damage == null) {
            $(".error-message").html("Please select a damage/defect");
            $(".help-block.damage").html("Please select a damage/defect");
            return false;
        }

        if ($("#image_override:checked").val() != "on") {
            App.errorView = "IMAGE";
            var proofOfPurchase = false,
                productImage = false;

            App.Collection.images.each(function(image) {
                if (image.attributes.type == "PROOF") {
                    proofOfPurchase = true;
                }
                if (image.attributes.type == "IMAGE") {
                    productImage = true;
                }
            });

            if (!proofOfPurchase) {
                $(".error-message").html("Please upload proof of purchase");
                return false;
            }

            if (!productImage) {
                $(".error-message").html("Please upload an image of damage/defect");
                return false;
            }
        }

		return true;
    },

	doSave: function(validate) {
        $(".error-message").html("");
        $(".help-block").html("");

	    var validSave = true;
	    if (validate) {
	        validSave = this.validate();
	    }

	    if (validSave) {
            var self = this;

            App.Model.warranty.attributes.name = $("#name").val();
            App.Model.warranty.attributes.email = $("#email").val();
            App.Model.warranty.attributes.phone = $("#phone").val();
            App.Model.warranty.attributes.address = $("#address").val();
            App.Model.warranty.attributes.style = $("#style").val();
            App.Model.warranty.attributes.color = $("#color").val();
            App.Model.warranty.attributes.damage = $("#damage").val();
            App.Model.warranty.attributes.notes = $("#notes").val();
            if ($("#image_override:checked").val() == "on") {
                App.Model.warranty.attributes.imageOverride = true;
            } else {
                App.Model.warranty.attributes.imageOverride = false;
            }

            App.Model.warranty.save({}, {
                wait: true,
                type: 'POST',
                success: function(model, response) {
                    self.enableSave(false);
                    if (self.saveStatus != "SAVE") {
                        App.View.saveStatusView.show(self.saveStatus);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus.statusText);
                }
            });
	    } else {
	        if (App.errorView == "FORM") {
	            App.View.formView.show();
	        } else if (App.errorView == "IMAGE") {
	            App.View.imagesView.show();
	        }

	    }
	},

    buttonSave: function() {
        this.saveStatus = "SAVE";
        this.doSave(false);
    },

    buttonPreAuthorized: function() {
        this.saveStatus = "PREAUTHORIZED";
        this.doSave(true);
    },

    buttonReceived: function() {
        this.saveStatus = "RECEIVED";
        this.doSave(true);
    },

    buttonAuthorized: function() {
        this.saveStatus = "AUTHORIZED";
        this.doSave(true);
    },

    buttonNotAuthorized: function() {
        this.saveStatus = "NOTAUTHORIZED";
        this.doSave(true);
    },

    buttonClosed: function() {
        this.saveStatus = "CLOSED";
        this.doSave(true);
    },

});

// ------------------------------------
//          SAVE STATUS MODAL
// ------------------------------------
App.View.SaveStatusView = Backbone.View.extend({
    el: $("#status_modal"),

    events: {
        "click .btn-success": "yes",
    },

    show: function (status) {
        this.status = status;
        this.$el.find(".modal-title").html("Set Status");
        this.$el.find(".modal-body p").html("Are you sure you want to set status to " + App.statuses[status] + "?");
	    this.$el.modal('show');
	},

    yes: function() {
        var self = this;

        App.Model.warranty.attributes.status = this.status;
        App.Model.warranty.save({}, {
            wait: true,
            type: 'POST',
            success: function(model, response) {
                if (response.returnStatus == "success") {
                    window.location.href = "/warranties";
                } else {
                    $(".error-message").html(response.returnStatus);
                    self.hide();
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert(textStatus.statusText);
            }
        });
    },

	hide: function() {
	    this.$el.modal('hide');
	},
});


// ------------------------------------
//              READY
// ------------------------------------
$(document).ready(function() {
    Backbone.emulateJSON = true;

	App.View.formView = new App.View.FormView();
	App.View.styleColorView = new App.View.StyleColorView();
	App.View.notesView = new App.View.NotesView();
	App.View.imagesView = new App.View.ImagesView();
	App.View.removeView = new App.View.RemoveView();
	App.View.uploadView = new App.View.UploadView();
	App.View.buttonView = new App.View.ButtonView();
	App.View.saveStatusView = new App.View.SaveStatusView();
	App.View.historyView = new App.View.HistoryView();

	App.View.formView.render();
	App.View.imagesView.render();
});