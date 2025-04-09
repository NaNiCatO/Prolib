import { AddBookData, BookData, BookDataAPI, BookEditable } from "./types";

type BookDataAPISingleOrMultiple = BookDataAPI | BookDataAPI[]

export const makeBookDataFromAPI = <T extends BookDataAPISingleOrMultiple>(bookDataAPI: T): T extends BookDataAPI[] ? BookData[] : BookData => {
    if (Array.isArray(bookDataAPI)) {
        const bookData: BookData[] = bookDataAPI.map(b => ({
            id: b.id,
            isCustomBook: b.data.isCustomBook,
            isFavorite: b.data.isFavorite,
            title: b.data.Title,
            authors: b.data.Authors,
            publisher: b.data.Publisher,
            publishedDate: b.data["Published Date"],
            description: b.data.Description,
            isbn10: b.data["ISBN 10"],
            isbn13: b.data["ISBN 13"],
            pageCount: b.data["Page Count"],
            categories: b.data.Categories,
            language: b.data.Language,
            coverUrl: b.data["Thumbnail URL"],
            rating: b.data["Average Rating"],
            ratingCount: b.data["Ratings Count"]
        }))

        return bookData as any
    } else {
        const bookData: BookData = {
            id: bookDataAPI.id,
            isCustomBook: bookDataAPI.data.isCustomBook,
            isFavorite: bookDataAPI.data.isFavorite,
            title: bookDataAPI.data.Title,
            authors: bookDataAPI.data.Authors,
            publisher: bookDataAPI.data.Publisher,
            publishedDate: bookDataAPI.data["Published Date"],
            description: bookDataAPI.data.Description,
            isbn10: bookDataAPI.data["ISBN 10"],
            isbn13: bookDataAPI.data["ISBN 13"],
            pageCount: bookDataAPI.data["Page Count"],
            categories: bookDataAPI.data.Categories,
            language: bookDataAPI.data.Language,
            coverUrl: bookDataAPI.data["Thumbnail URL"],
            rating: bookDataAPI.data["Average Rating"],
            ratingCount: bookDataAPI.data["Ratings Count"]
        }

        return bookData as any
    }
}

export const updateBookDataFromEditable = (bookData: BookData, bookDataEditable: BookEditable): BookData => {
    const b = bookData
    const be = bookDataEditable
    const newBookData: BookData = { ...b, ...be }

    return newBookData
}

export const makeBookEditable = (book: BookData): BookEditable => {
    const bookEditable: BookEditable = {
        id: book.id,
        Title: book.title,
        Authors: book.authors,
        Publisher: book.publisher,
        "Published Date": book.publishedDate,
        Description: book.description,
        "Page Count": book.pageCount,
        Categories: book.categories,
        Language: book.language,
        "Thumbnail URL": book.coverUrl
    }

    return bookEditable
}

export const makeAPIFromBookData = (book: BookData): BookDataAPI => {
    const bookDataApi: BookDataAPI = {
        id: book.id,
        data: {
            isCustomBook: book.isCustomBook,
            isFavorite: book.isFavorite,
            Title: book.title,
            Authors: book.authors,
            Publisher: book.publisher,
            "Published Date": book.publishedDate,
            Description: book.description,
            "ISBN 10": book.isbn10 ?? "",
            "ISBN 13": book.isbn13 ?? "",
            "Page Count": book.pageCount,
            Categories: book.categories,
            Language: book.language,
            "Thumbnail URL": book.coverUrl,
            "Average Rating": book.rating,
            "Ratings Count": book.ratingCount
        }
    }

    return bookDataApi
}

export const makeAPIFromAddBookData = (book: AddBookData): BookDataAPI => {
    const bookDataApi: BookDataAPI = {
        id: "",
        data: {
            isCustomBook: true,
            isFavorite: false,
            Title: book.title,
            Authors: book.authors,
            Publisher: book.publisher,
            "Published Date": book.publishedDate,
            Description: book.description,
            "ISBN 10": "",
            "ISBN 13": "",
            "Page Count": book.pageCount,
            Categories: book.categories,
            Language: book.language,
            "Thumbnail URL": book.coverUrl,
            "Average Rating": null,
            "Ratings Count": null
        }
    }

    return bookDataApi
}

export const findCustomBooks = (allBooks: BookDataAPI[]) => {
    return allBooks.filter(b => b.data.isCustomBook)
}

export const findFavoriteBooks = (allBooks: BookDataAPI[]) => {
    return allBooks.filter(b => b.data.isFavorite)
}