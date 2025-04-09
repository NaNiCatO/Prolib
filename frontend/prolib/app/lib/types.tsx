// export type BookData = {
//     id: string;
//     title: string;
//     author: string;
//     cover: string;
//     genre: string[];
//     rating: number | null;
//     ratingCount: number | null;
// }

export type BookData = {
    id: string
    isCustomBook: boolean
    isFavorite: boolean
    title: string
    authors: string[]
    publisher: string
    publishedDate: string
    description: string
    isbn10?: string
    isbn13?: string
    pageCount: string
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
    pageCount: string
    categories: string[]
    language: string
    coverUrl: string
}

export type AddBookData = {
    title: string
    authors: string[]
    publisher: string
    publishedDate: string
    description: string
    pageCount: string
    categories: string[]
    language: string
    coverUrl: string
}

export type BookDataAPI = {
    "id": string
    "data": {
        "isCustomBook": boolean,
        "isFavorite": boolean,
        "Title": string,
        "Authors": string[],
        "Publisher": string,
        "PublishedDate": string,
        "Description": string,
        "ISBN10": string,
        "ISBN13": string,
        "PageCount": number | string,
        "Categories": string[],
        "Language": string,
        "Thumbnail": string,
        "AvgRating": number | null,
        "PeopleRated": number | null,
        "PreviewLink"?: string,
        "InfoLink"?: string
    }
}