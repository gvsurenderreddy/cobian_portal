from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings

if settings.DEBUG:
    import sqlite3 as db_engine
else:
    import psycopg2 as db_engine
    import psycopg2.extras as db_extras

# JSON
import ujson as json

# LOGGING
import logging

logger = logging.getLogger("api.report")


# ------------------------------------------
#               WARRANTY
# ------------------------------------------
def api_report_warranty(request):
    try:
        report = request.GET.get("report", "style")

        if report == "style":
            sql_select = "SELECT style, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY style"
            sql_order_by = "ORDER BY count DESC"

        elif report == "style-color":
            sql_select = "SELECT style, color, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY style, color"
            sql_order_by = "ORDER BY count DESC, style, color"

        elif report == "style-damage":
            sql_select = "SELECT style, damage, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY style, damage"
            sql_order_by = "ORDER BY count DESC, style, damage"

        elif report == "style-color-damage":
            sql_select = "SELECT style, color, damage, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY style, color, damage"
            sql_order_by = "ORDER BY count DESC, style, color, damage"

        elif report == "damage":
            sql_select = "SELECT damage, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY damage"
            sql_order_by = "ORDER BY count DESC"

        elif report == "damage-style":
            sql_select = "SELECT style, damage, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY damage, style"
            sql_order_by = "ORDER BY count DESC, damage, style"

        elif report == "damage-color":
            sql_select = "SELECT color, damage, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY damage, color"
            sql_order_by = "ORDER BY count DESC, damage, color"

        elif report == "damage-style-color":
            sql_select = "SELECT style, color, damage, count(id) as count FROM db_warranty"
            sql_group_by = "GROUP BY damage, style, color"
            sql_order_by = "ORDER BY count DESC, damage, style, color"

        sql_where = get_warranty_request_sql(request)

        sql = "{} {} {} {}".format(sql_select, sql_where, sql_group_by, sql_order_by)

        results = execute_sql(sql)

        return_list = []
        count = 0
        for result in results:
            count += 1
            result_dict = {
                    "id": count,
                    "count": result["count"]
                }

            if report == "style":
                result_dict["style"] = result["style"]
            elif report == "damage":
                result_dict["damage"] = result["damage"]
            elif report == "style-color":
                result_dict["style"] = result["style"]
                result_dict["color"] = result["color"]
            elif report == "style-damage" or report == "damage-style":
                result_dict["style"] = result["style"]
                result_dict["damage"] = result["damage"]
            elif report == "style-color-damage" or report == "damage-style-color":
                result_dict["style"] = result["style"]
                result_dict["color"] = result["color"]
                result_dict["damage"] = result["damage"]
            elif report == "damage-color":
                result_dict["damage"] = result["damage"]
                result_dict["color"] = result["color"]

            return_list.append(result_dict)

        return HttpResponse(json.dumps(return_list), content_type="application/json")

    except Exception as e:
        logger.error("api_report_warranty_style: {}".format(e))
        return HttpResponseServerError(e)


def get_warranty_request_sql(request):
    status = request.GET.get("status", None)
    status_date = "status_date"
    if status == "VALID":
        status_date = "valid_date"
    elif status == "VERIFIED":
        status_date = "verified_date"
    elif status == "CLOSED":
        status_date = "closed_date"
    elif status == "ALL":
        status = None

    date_range = get_date_range(request, status_date)

    if status or date_range:
        sql = "WHERE "
        if status:
            sql += "status='{}' ".format(status)

        if date_range:
            if status:
                sql += "AND "
            sql += date_range
        return sql
    else:
        return ""


# ------------------------------------------
#               HELPERS
# ------------------------------------------
def get_date_range(request, date_to_query):
    date_range = request.GET.get("date_range", None)

    if date_range == "RANGE":
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        date_from = "{} 00:00:00".format(start_date)
        date_to = "{} 23:59:59".format(end_date)

        return "{0} >= '{1}' AND {0} <= '{2}' ".format(date_to_query, date_from, date_to)
    else:
        return ""


# ------------------------------------------
#              EXECUTE SQL
# ------------------------------------------
def execute_sql(sql):
    connection = None

    try:
        if settings.DEBUG:
            connection = db_engine.connect(settings.DB_NAME)
            connection.row_factory = db_engine.Row
            cursor = connection.cursor()
        else:
            connection = db_engine.connect(database=settings.DB_NAME,
                                           user=settings.DB_USER,
                                           password=settings.DB_PASSWORD)
            cursor = connection.cursor(cursor_factory=db_extras.DictCursor)

        cursor.execute(sql)

        return cursor.fetchall()

    except db_engine.DatabaseError as e:
        raise e
    except Exception as e:
        raise e

    finally:
        if connection:
            connection.close()


def api_report_test(request):
    try:
        sql = "SELECT * FROM db_warranty "
        sql += get_warranty_request_sql(request)
        sql += "ORDER BY status_date DESC"

        results = execute_sql(sql)

        return_list = []
        for result in results:
            return_list.append({
                "id": result["id"],
                "status": result["status"],
                "style": result["style"],
                "statusDate": result["status_date"],
                "validDate": result["valid_date"],
                "verifiedDate": result["verified_date"],
                "closedDate": result["closed_date"],
            })

        return HttpResponse(json.dumps(return_list), content_type="application/json")

    except Exception as e:
        logger.error("api_report_test: {}".format(e))
        return HttpResponseServerError(e)
