def average_books_per_year_by_author(df):
    # Group by author, count books per year, then calculate the average
    average_books = df.groupby('author_names').apply(lambda x: x['first_publish_year'].nunique() / x['title'].count())
    return average_books.reset_index(name='average_books_per_year')


def books_per_year_by_author(df):
    # Group by author and year, then count the number of books
    books_per_year = df.groupby(['author_names', 'first_publish_year']).size().reset_index(name='book_count')
    return books_per_year