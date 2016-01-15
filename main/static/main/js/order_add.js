$(document).ready(function() {
    $("#product_style").change(function() {
        bindProductItemGrid($(this).val());
    });
    
    $("#order_add_submit").click(function() {
        var orderItems = [];
        $.each($("input"), function(index) {
            var id = $(this).data("id"),
                quantity = $(this).val();
                        
            if ($.isNumeric(quantity)) {
                qty = parseInt(quantity);
                if (qty > 0) {
                    var sku = {
                        id: id,
                        quantity: quantity
                    }
                    orderItems.push(sku);
                }
            }
        });
        
        if (orderItems.length > 0) {
            debugger;
            var url = "/dealer/order/detail/add/" + $("#product_item_grid").data("id") + "/";
            $.ajax({
                type: "GET",
                url: url,
                data: {
                    order_items: JSON.stringify(orderItems)
                    },
                dataType: "json",
                success: function(data) {
                    window.location.href = "/dealer/order/" + $("#product_item_grid").data("id");
                },
                error: function(jqXHR, textStatus, errorThrown) {

                }
            });
        }
    });
    
});

function bindProductItemGrid(productStyleId) {
    if (productStyleId > 0) {
        $.ajax({
            type: "GET",
            url: "/api/product/items/grid/" + productStyleId + "/",
            data: { },
            dataType: "json",
            success: function(data) {
                var html = "";
                var maxIndex = 0;
                            
                $.each(data, function(index) {
                    if (data[index]["skus"].length > maxIndex) {
                        maxIndex = data[index]["skus"].length;
                    }
                });
                
                html += '<div class="row">';
                $.each(data, function(index) {
                    var skus = data[index]["skus"];
                    
                    html += '<div class="col-sm-2">';
                    html += '<div class="panel">';
                    html += '    <div class="panel-heading">' + data[index]["description"] + '</div>';
                    html += '   <ul class="list-group">';
                    var count = 0;
                    $.each(skus, function(index) {
                        count++;
                        html += '<li class="list-group-item">';
                        html += '   <div class="form-horizontal"><div class="form-group">';
                        html += '       <label class="control-label">' + skus[index]["size"] + '</label>';
                        html += '       <input class="form-control" type="number" min="0" placeholder="0" data-id="' + skus[index]["id"] + '" />';
                        html += '   </div></div>';
                        html += '</li>';
                    });
                    for (var i=count; i < maxIndex; i++) {
                        html += '<li class="list-group-item">&nbsp;</li>';
                    }
                    html += '   </ul>';
                    html += '</div>';
                    html += '</div>';
                });
                html += '</div>';
                $("#product_item_grid").html(html);
                $("#order_add_submit").css("display", "inline");
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
                $("#order_add_submit").css("display", "none");
                $("#product_item_grid").html("");
            }
        });
    } else {
        $("#order_add_submit").css("display", "none");
        $("#product_item_grid").html("");
    }
}