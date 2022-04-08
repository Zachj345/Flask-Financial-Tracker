import json
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Piece, Inventory
from . import db


views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            title = 'untitled-item'
        prodcost = request.form.get('prodcost')
        if prodcost == '':
            prodcost = 0
        price = request.form.get('price')
        if price == '':
            price = 0

        smalls = request.form.get('smalls')
        if not smalls:
            smalls = 0
        meds = request.form.get('mediums')
        if not meds:
            meds = 0
        larges = request.form.get('larges')
        if not larges:
            larges = 0
        xl = request.form.get('xl')
        if not xl:
            xl = 0
        xxl = request.form.get('xxl')
        if not xxl:
            xxl = 0

        stock = Inventory(small=smalls, med=meds, large=larges, xl=xl, xxl=xxl)
        new_piece = Piece(title=title, prodcost=prodcost,
                          price=price)
        db.session.add(new_piece)
        db.session.add(stock)
        db.session.commit()

        flash('Items successfully entered!', category='success')
        return redirect(url_for('views.inventory'))

    return render_template('home.html', user=current_user)


@views.route('/delete-user/<string:username>')
def delete_acct(username):
    acct = User.query.filter_by(username=username).first()
    db.session.delete(acct)
    db.session.commit()
    return 'account deleted successfully!', 200


@views.route('/delete/<int:id>')
def delete_content(id):
    item = Piece.query.filter_by(id=id).first()
    inventory = Inventory.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.delete(inventory)
    db.session.commit()

    return redirect(url_for('views.inventory'))


@views.route('/add-small/<int:id>', methods=['GET', 'POST'])
def add_small(id):
    item = Inventory.query.filter_by(id=id).first()
    item.small += 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/add-med/<int:id>', methods=['GET', 'POST'])
def add_med(id):
    item = Inventory.query.filter_by(id=id).first()
    item.med += 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/add-large/<int:id>', methods=['GET', 'POST'])
def add_large(id):
    item = Inventory.query.filter_by(id=id).first()
    item.large += 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/add-xl/<int:id>', methods=['GET', 'POST'])
def add_xl(id):
    item = Inventory.query.filter_by(id=id).first()
    item.xl += 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/add-xxl/<int:id>', methods=['GET', 'POST'])
def add_xxl(id):
    item = Inventory.query.filter_by(id=id).first()
    item.xxl += 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/sub-small/<int:id>', methods=['GET', 'POST'])
def subtract_small(id):
    item = Inventory.query.filter_by(id=id).first()
    item.small -= 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/sub-med/<int:id>', methods=['GET', 'POST'])
def subtract_med(id):
    item = Inventory.query.filter_by(id=id).first()
    item.med -= 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/sub-large/<int:id>', methods=['GET', 'POST'])
def subtract_large(id):
    item = Inventory.query.filter_by(id=id).first()
    item.large -= 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/sub-xl/<int:id>', methods=['GET', 'POST'])
def subtract_xl(id):
    item = Inventory.query.filter_by(id=id).first()
    item.xl -= 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


@views.route('/sub-xxl/<int:id>', methods=['GET', 'POST'])
def subtract_xxl(id):
    item = Inventory.query.filter_by(id=id).first()
    item.xxl -= 1
    db.session.commit()
    return redirect(url_for('views.inventory'))


def item_sum(id):
    lst = []
    item = Inventory.query.filter_by(id=id).first()
    lst.append(item.small)
    lst.append(item.med)
    lst.append(item.large)
    lst.append(item.xl)
    lst.append(item.xxl)
    try:
        item_sum = sum(lst)
        piece_items = Piece.query.all()
        price_list = [x.price for x in piece_items]
        selection = [i.id for i in piece_items]
        price_selection = {i: j for i, j in zip(selection, price_list)}

        # print(lst, price_selection, piece_items)

        return item_sum * price_selection[id]
    except TypeError:
        return 0
    except KeyError:
        pass


def sum_prod_cost(id):
    lst = []
    item = Inventory.query.filter_by(id=id).first()
    lst.append(item.small)
    lst.append(item.med)
    lst.append(item.large)
    lst.append(item.xl)
    lst.append(item.xxl)
    try:
        item_sum = sum(lst)
        piece_items = Piece.query.all()
        product_cost = [x.prodcost for x in piece_items]
        selection = [i.id for i in piece_items]
        prod_selection = {i: j for i, j in zip(selection, product_cost)}

        return item_sum * prod_selection[id]
    except TypeError:
        return 0
    except KeyError:
        pass


def item_count(id):
    lst = []
    items = Inventory.query.filter_by(id=id).first()
    lst.append(items.small)
    lst.append(items.med)
    lst.append(items.large)
    lst.append(items.xl)
    lst.append(items.xxl)
    try:
        item_sum_lst = sum(lst)
        return item_sum_lst
    except TypeError:
        return 0
    except KeyError:
        pass


@views.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    pieces = Piece.query.all()
    stock = Inventory.query.all()
    individual = [list(i) for i in zip(pieces, stock)]
    # print(individual, User.query.all())
    return render_template('inventory.html', user=current_user, pieces=pieces, stock=stock,
                           sum_prod_cost=sum_prod_cost, item_sum=item_sum, total_instock=item_count,
                           both_dbs=individual)
