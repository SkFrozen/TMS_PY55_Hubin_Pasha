from flask import Flask, jsonify, redirect, render_template, request
from models.base import Base, engine, engine2
from models.categories import Category
from models.goods import Good
from models.orders import Order
from models.providers import Provider
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

metadata = Base.metadata

app = Flask(__name__)
session_pool = sessionmaker(bind=engine)


@app.route("/", methods=["GET", "POST"])
def home():
    with session_pool() as session:
        categories = (
            session.query(
                Category.name,
                func.count(Good.name),
                func.sum(Good.cost),
            )
            .join(Good, Category.id == Good.category_num)
            .group_by(Category.id)
            .all()
        )
        orders = (
            session.query(func.sum(Good.cost), func.count(Order.id))
            .join(Order, Good.id == Order.good_num)
            .all()
        )
    return render_template(
        "index.html", route="/", categories=categories, orders=orders
    )


@app.route("/errors")
def errors():
    return render_template("/errors.html")


"""START goods view"""


@app.route("/goods", methods=["GET", "POST"])
def get_goods():
    if request.method == "POST":
        with session_pool() as session:
            json_data = Good.get_info(id=request.json.get("id"), session=session)
            json = jsonify(json_data)
            return json
    else:
        with session_pool() as session:
            goods = (
                session.query(Good, Provider.company_name, Category.name)
                .filter(Good.provider_num == Provider.id)
                .filter(Good.category_num == Category.id)
                .all()
            )
            providers = session.query(Provider).all()
            categories = session.query(Category).all()
        return render_template(
            "goods.html",
            goods=goods,
            route="goods",
            providers=providers,
            categories=categories,
        )


@app.route("/goods/add", methods=["POST"])
def add_good():
    if request.method == "POST":
        try:
            with session_pool() as session:
                Good.add(
                    name=request.form["name"],
                    cost=request.form["cost"],
                    provider=request.form["provider"],
                    category=request.form["category"],
                    session=session,
                )
                session.commit()
        except Exception as e:
            return render_template("errors.html", e=e, route="/goods")
    return redirect("/goods")


@app.route("/goods/update", methods=["POST"])
def update_good():
    if request.method == "POST":
        try:
            with session_pool() as session:
                good = Good.get_good_by_id(
                    id=request.form.get("good_id"), session=session
                )
                good.update(
                    name=request.form.get("name"),
                    cost=request.form.get("cost"),
                    provider=request.form.get("provider"),
                    category=request.form.get("category"),
                    session=session,
                )
                session.commit()
            return redirect("/goods")
        except ValueError as e:
            return render_template("errors.html", e=e, route="/goods")


@app.route("/goods/delete/<id_g>", methods=["GET"])
def delete_good(id_g):
    with session_pool() as session:
        try:
            good = Good.get_good_by_id(id=id_g, session=session)
            good.delete(session=session)
            session.commit()
        except Exception as e:
            return redirect("/orders")
    return redirect("/goods")


"""START providers view"""


@app.route("/providers", methods=["GET", "POST"])
def get_providers():
    if request.method == "POST":
        with session_pool() as session:
            json_data = Provider.get_info(id=request.json.get("id"), session=session)
            json = jsonify(json_data)
            return json
    else:
        with session_pool() as session:
            providers = session.query(Provider).all()

        return render_template("providers.html", providers=providers, route="providers")


@app.route("/providers/add", methods=["POST"])
def add_provider():
    if request.method == "POST":
        try:
            with session_pool() as session:
                Provider.add(
                    first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                    email=request.form.get("email"),
                    company_name=request.form.get("company_name"),
                    session=session,
                )
                session.commit()
            return redirect("/providers")
        except Exception as e:
            return render_template("errors.html", e=e, route="/providers")


@app.route("/providers/update", methods=["POST"])
def update_privder():
    if request.method == "POST":
        try:
            with session_pool() as session:
                provider = Provider.get_provider_by_id(
                    id=request.form.get("provider_id"), session=session
                )
                provider.update(
                    first_name=request.form.get("first_name"),
                    last_name=request.form.get("last_name"),
                    email=request.form.get("email"),
                    company_name=request.form.get("company_name"),
                    session=session,
                )
                session.commit()
            return redirect("/providers")
        except Exception as e:
            return render_template("errors.html", e=e, route="/providers")


@app.route("/providers/delete/<id_p>", methods=["GET"])
def delete_provider(id_p):
    with session_pool() as session:
        try:
            provider = Provider.get_provider_by_id(id=id_p, session=session)
            provider.delete(session=session)
            session.commit()
            return redirect("/providers")
        except Exception as e:
            return render_template("errors.html", route="/providers", e=e)


"""START orders view"""


@app.route("/orders", methods=["GET", "POST"])
def get_orders():
    if request.method == "POST":
        with session_pool() as session:
            json_data = Order.get_info(id=request.json.get("id"), session=session)
            json = jsonify(json_data)
            return json
    else:
        with session_pool() as session:
            orders = (
                session.query(Order, Good.name).filter(Order.good_num == Good.id).all()
            )
            goods = session.query(Good).all()
        return render_template(
            "orders.html", orders=orders, goods=goods, route="orders"
        )


@app.route("/orders/add", methods=["POST"])
def add_order():
    if request.method == "POST":
        try:
            with session_pool() as session:
                Order.add(
                    name=request.form.get("name"),
                    address=request.form.get("address"),
                    notes=request.form.get("notes"),
                    email=request.form.get("email"),
                    status=request.form.get("status"),
                    good_id=request.form.get("good_id"),
                    session=session,
                )
                session.commit()
            return redirect("/orders")
        except Exception as e:
            return render_template("errors.html", e=e, route="/orders")


@app.route("/orders/update", methods=["POST"])
def update_order():
    if request.method == "POST":
        try:
            with session_pool() as session:
                order = Order.get_order_by_id(
                    id=request.form.get("order_id"), session=session
                )
                order.update(
                    name=request.form.get("name"),
                    address=request.form.get("address"),
                    notes=request.form.get("notes"),
                    email=request.form.get("email"),
                    status=request.form.get("status"),
                    good_id=request.form.get("good"),
                    session=session,
                )
                session.commit()
            return redirect("/orders")
        except Exception as e:
            return render_template("errors.html", e=e, route="/orders")


@app.route("/orders/delete/<o_id>", methods=["GET"])
def delete_order(o_id):
    with session_pool() as session:
        order = Order.get_order_by_id(id=o_id, session=session)
        order.delete(session=session)
        session.commit()
    return redirect("/orders")


"""START categories view"""


@app.route("/categories", methods=["GET", "POST"])
def get_categories():
    if request.method == "POST":
        with session_pool() as session:
            category = (
                session.query(Category).filter_by(id=request.json.get("id")).first()
            )

            return jsonify({"id": category.id, "name": category.name})

    with session_pool() as session:
        categories = session.query(Category).all()

    return render_template("categories.html", categories=categories, route="category")


@app.route("/category/delete/<c_id>")
def delete_category(c_id):
    try:
        with session_pool() as session:
            session.query(Category).filter_by(id=c_id).delete()
            session.commit()
        return redirect("/categories")
    except Exception as e:
        return render_template("errors.html", e=e, route="/categories")


@app.route("/categories/update", methods=["GET", "POST"])
def update_category():
    if request.method == "POST":
        with session_pool() as session:
            category = (
                session.query(Category)
                .filter_by(id=request.form.get("category_id"))
                .first()
            )
            category.name = request.form.get("name")
            session.commit()
        return redirect("/categories")


@app.route("/categories/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        if request.form.get("name") != "":
            with session_pool() as session:
                session.add(Category(name=request.form.get("name")))
                session.commit()
            return redirect("/categories")
        else:
            error = "Error: an empty field is prohibited"
            return render_template("errors.html", route="/categories", error=error)


if __name__ == "__main__":
    # metadata.create_all(engine)
    app.run("localhost", 8000)
