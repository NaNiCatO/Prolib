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
    Title: string
    Authors: string[]
    Publisher: string
    "Published Date": string
    Description: string
    "Page Count": string
    Categories: string[]
    Language: string
    "Thumbnail URL": string
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
        "Published Date": string,
        "Description": string,
        "ISBN 10": string,
        "ISBN 13": string,
        "Page Count": string,
        "Categories": string[],
        "Language": string,
        "Thumbnail URL": string,
        "Average Rating": number | null,
        "Ratings Count": number | null,
        "Preview Link"?: string,
        "Info Link"?: string
    }
};
