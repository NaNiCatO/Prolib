export type BookData = {
    id: string;
    title: string;
    author: string;
    cover: string;
    genre: string[];
    rating: number | null;
    ratingCount: number | null;
}

export type BookData2 = {
    id: string
    isCustomBook: boolean
    isFavorite: boolean
    title: string
    authors: string[]
    publisher: string
    publishedDate: string
    description: string
    isbn10: string
    isbn13: string
    pageCount: number
    categories: string[]
    language: string
    coverUrl: string
    rating: number | null
    ratingCount: number | null
}

export type BookEditable = {
    id: string
    title: string
    authors: string[]
    publisher: string
    publishedDate: string
    description: string
    isbn10: string
    isbn13: string
    pageCount: number
    categories: string[]
    language: string
    coverUrl: string
}