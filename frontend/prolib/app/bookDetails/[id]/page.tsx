"use client"
import React, { ChangeEvent, use, useEffect, useState } from 'react';
import { ArrowLeft, Heart, Share2, Bookmark } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import DeleteBookAlertDialog from '@/app/ui/delete-book-alert-dialog';
import { EditBookSheet } from '@/app/ui/edit-book-sheet';
import { BookData, BookDataAPI } from '@/app/lib/types';
import { makeAPIFromBookData, makeBookDataFromAPI, makeBookEditable, updateBookDataFromEditable } from '@/app/lib/bookDataFormatting';
import fallbackImage from "@/public/fallbackImage.png"


// interface BookData {
//     id: string;
//     isCustomBook: boolean
//     isFavorite: boolean
//     title: string;
//     author: string;
//     coverImage: string;
//     description: string;
//     releaseDate: string;
//     publisher: string;
//     language: string;
//     format: string;
//     isbn: string;
//     pages: number;
//     categories: string[];
// }

const defaultBookData: BookData = {
    id: "",
    isCustomBook: false,
    isFavorite: false,
    title: "",
    authors: [],
    publisher: "",
    publishedDate: "",
    description: "",
    isbn10: "",
    isbn13: "",
    pageCount: "",
    categories: [],
    language: "",
    coverUrl: "",
    rating: null,
    ratingCount: null
}

export default function BookDetailPage({ params }: { params: Promise<{ id: string }> }) {
    // Example book data - in a real app, you'd fetch this based on route params
    // let book: BookData = {
    //     id: '1',
    //     isCustomBook: true,
    //     isFavorite: false,
    //     title: 'Debt — The First 5,000 Years',
    //     authors: ['David Graeber'],
    //     coverUrl: '/diary.jpg', // Placeholder for demo - replace with actual image path
    //     description: `Diminutive rooms, grand possibilities. Small Homes, Grand Living shows how to make use of a limited space and turn a small apartment into a design marvel! Here anthropologist David Graeber presents a stunning reversal of conventional wisdom. He shows that before there was money, there was debt. For more than 5,000 years, since the beginnings of the first agrarian empires, humans have used elaborate credit systems to buy and sell goods—that is, long before the invention of coins or cash.`,
    //     publishedDate: 'May 2017',
    //     publisher: 'Melville House',
    //     language: 'English',
    //     isbn10: "",
    //     isbn13: '978-3-89955-598-8',
    //     pageCount: "256",
    //     categories: ['History', 'Economics', 'Anthropology'],
    //     rating: 3.5,
    //     ratingCount: 86
    // };

    const router = useRouter()
    const parameters = use(params)

    const { id } = parameters
    console.log(id)

    const [book, setBook] = useState<BookData>(defaultBookData)
    const [isFavorite, setIsFavorite] = useState(book?.isFavorite ?? false)
    const [bookEditData, setBookEditData] = useState(makeBookEditable(book))

    // Fetch book based on book id here
    useEffect(() => {
        async function fetchBook() {
            try {
                const response = await fetch(new URL(`http://localhost:8000/books/${id}`));
                console.log(response, "response")
                const data: BookDataAPI = await response.json();
                console.log(data, "data")
                const formattedData: BookData = makeBookDataFromAPI(data)
                console.log(formattedData, "formattedData")
                setBook(formattedData);
                setBookEditData(makeBookEditable(formattedData))
            } catch (error) {
                console.error('Error fetching books:', error);
            }
        }

        fetchBook();
    }, []);

    const handleToggleFavorites = async () => {
        setIsFavorite(b => !b)

        // update backend data
        const res = await fetch(new URL(`http://localhost:8000/books/${id}/favorite`), { method: "PATCH" })
        console.log(id)
        console.log(res.ok)
    }

    const handleChangeEvent = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const id: string = e.target.id
        const value = e.target.value
        setBookEditData(b => {
            return { ...b, [id]: value }
        })
        console.log(bookEditData)
    }

    const handleDeleteBook = async () => {
        // update backend data
        const res = await fetch(new URL(`http://localhost:8000/books/${id}`), { method: "DELETE" })
        console.log(id)
        console.log(res.ok)

        router.back()
        // Display toast
    }

    const handleEditBook = async () => {
        // book = updateBookDataFromEditable(book, bookEditData)
        // const bookApi = makeAPIFromBookData(book)
        // update backend data
        // formDataBookUpdate.append('update', JSON.stringify(bookApi));

        const bookEdited: any = { ...bookEditData }
        delete bookEdited.id

        const res = await fetch(new URL(`http://localhost:8000/books/${id}`), {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookEdited)
        })

        console.log(id)
        console.log(res.ok)
        console.log(bookEdited)

        // router.prefetch(`/bookDetails/${id}`)
        router.replace(`/bookDetails/${id}`)
        // Display toast
    }

    return (
        <div className="container mx-auto py-8 px-4">
            <div className="mb-6">
                <Button variant="ghost" className="pl-0" onClick={() => router.back()}>
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Back to Books
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Book Cover - Left Column */}
                <div className="md:col-span-1">
                    <div className="bg-white p-4 shadow-lg rounded-lg">
                        <div className="flex flex-wrap justify-end mb-4">
                            <Button variant="outline" size="sm" onClick={handleToggleFavorites}>
                                <Heart className={`h-4 w-4 ${isFavorite && "fill-red-500 stroke-red-500"}`} />
                                {/* Favorite */}
                            </Button>
                            {/* <Button variant="outline" size="sm">
                                <Share2 className="h-4 w-4 mr-2" />
                                Share
                            </Button> */}
                            {/* <Button variant="outline" size="sm">
                                <Bookmark className="h-4 w-4 mr-2" />
                                Save
                            </Button> */}
                        </div>
                        <div className="relative h-100 w-auto">
                            <Image
                                src={(book.coverUrl == "N/A" || book.coverUrl == "") ? fallbackImage.src : book.coverUrl}
                                alt={`${book.title} by ${book.authors.join(", ")}`}
                                fill={true}
                                className="w-full object-contain aspect-[3/4] rounded"
                            />
                        </div>
                    </div>
                </div>

                {/* Book Details - Right Column */}
                <div className="md:col-span-2">
                    <h1 className="text-3xl font-bold mb-1">{book.title}</h1>
                    <h2 className="text-xl text-gray-600 mb-4">by {book.authors.join(", ")}</h2>

                    <div className="flex flex-wrap gap-2 mb-6">
                        {book.categories.map(category => (
                            <Badge key={category} variant="secondary">{category}</Badge>
                        ))}
                    </div>

                    <div className="max-w-none mb-8">
                        <p className="text-gray-700">{book.description}</p>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-y-4 gap-x-8 mt-8 border-t pt-6">
                        <div>
                            <h3 className="text-sm font-medium text-gray-500">Editor</h3>
                            <p>{book.publisher}</p>
                        </div>
                        <div>
                            <h3 className="text-sm font-medium text-gray-500">Published Date</h3>
                            <p>{book.publishedDate}</p>
                        </div>
                        <div>
                            <h3 className="text-sm font-medium text-gray-500">Features</h3>
                            <p>Full color, {book.pageCount} pages</p>
                        </div>
                        <div>
                            <h3 className="text-sm font-medium text-gray-500">Rating</h3>
                            <p>{book.rating == null ? "None" : `${book.rating}/5`}</p>
                        </div>
                        <div>
                            <h3 className="text-sm font-medium text-gray-500">Language</h3>
                            <p>{book.language}</p>
                        </div>
                        <div>
                            <h3 className="text-sm font-medium text-gray-500">ISBN</h3>
                            <p>{book.isbn13}</p>
                        </div>
                    </div>

                    {
                        book.isCustomBook &&
                        <div className="mt-8 flex flex-col sm:flex-row gap-4">
                            <EditBookSheet text='Edit Book' book={bookEditData} changeEventHandler={handleChangeEvent} submitHandler={handleEditBook} />
                            <DeleteBookAlertDialog text='Delete Book' clickHandler={handleDeleteBook} />
                        </div>
                    }

                </div>
            </div>
        </div>
    );
};