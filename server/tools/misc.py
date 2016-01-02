def count_page(model, per_page):
    count = model.query.count()
    pages, residual = divmod(count, per_page)
    if residual != 0:
        pages += 1
    return pages

