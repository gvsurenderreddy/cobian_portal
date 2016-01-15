$(document).ready(function() {
    $("#product_style").change(function() {
        $("#product_item").hide();
        $("#product_sku").hide();
        $("#order_detail_submit").hide();
        bindProductItemList($(this).val());
    });
    
    $("#product_item").change(function() {
        $("#product_sku").hide();
        $("#order_detail_submit").hide();
        bindProductSkuList($(this).val());
    });
    
    $("#product_sku").change(function() {
        $("#order_detail_submit").show();
    });
    
    var productStyleId = parseInt($("#product_style").val());
    if (productStyleId > 0) {
        bindProductItemList(productStyleId);
    } else {
        $("#product_item").hide();
        $("#product_sku").hide();
        $("#order_detail_submit").hide();
    }
});

function bindProductItemList(productStyleId) {
    $.ajax({
        type: "GET",
        url: "/api/product/items/" + productStyleId + "/",
        data: { },
        dataType: "json",
        success: function(data) {
            var jsonData = eval(data);
            var productItemId = parseInt($("#product_item_id").val());
            var itemFound = false;
            
            var optionsValues = '<option value="0">Select Item</option>';
            $.each(jsonData, function(index) {
                var selected = "";
                if (jsonData[index].id == productItemId) {
                    selected = 'selected="selected"';
                    itemFound = true;
                }
                optionsValues += '<option value="' + jsonData[index].id + '"' + selected + '>' + jsonData[index].item_number + ' - ' + jsonData[index].description + '</option>'; 
            });
            $("#product_item").html(optionsValues);
            $("#product_item").show();
            if (itemFound) bindProductSkuList(productItemId);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#product_item").hide();
            $("#product_sku").hide();
            $("#order_detail_submit").hide();
        }
    });
}

function bindProductSkuList(productItemId) {
    $.ajax({
        type: "GET",
        url: "/api/product/skus/" + productItemId + "/",
        data: { },
        dataType: "json",
        success: function(data) {
            var jsonData = eval(data);
            var productSkuId = parseInt($("#product_sku_id").val());
            var skuFound = false;
            
            var optionsValues = '<option value="0">Select Size</option>';
            $.each(jsonData, function(index) {
                var selected = "";
                if (jsonData[index].id == productSkuId) {
                    selected = 'selected="selected"';
                    skuFound = true;
                }
                optionsValues += '<option value="' + jsonData[index].id + '"' + selected + '>' + jsonData[index].size + ' - $' + jsonData[index].wholesale + '</option>'; 
            });
            $("#product_sku").html(optionsValues);
            $("#product_sku").show();
            if (skuFound) $("#order_detail_submit").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#product_sku").hide();
            $("#order_detail_submit").hide();
        }
    });
}