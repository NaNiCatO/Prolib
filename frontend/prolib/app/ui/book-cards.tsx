import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { BookData } from "../lib/types";
import Image from "next/image";
import StarRating from "./star-rating";
import { redirect, RedirectType } from "next/navigation";
import fallbackImage from "@/public/fallbackImage.png"

export default function BookCards({ books }: { books: BookData[] }) {
    // console.log(books, "books")
    return (
        <div className="ml-4 mr-4 flex flex-wrap justify-start gap-4">
            {books.length == 0 ? <h1 className="text-4xl ml-3">Looks like it's empty here...</h1> :
                books.map((book) => (
                    <Card key={book.id} className="shadow-md w-52 hover:bg-accent hover:text-accent-foreground select-none" onClick={() => redirect(`/bookDetails/${book.id}`, RedirectType.push)}>
                        <CardContent>
                            <div className="flex justify-center w-full h-52">
                                {/* <Image src={fallbackImage.src} */}
                                <Image src={(book.coverUrl == "N/A" || book.coverUrl == "") ? fallbackImage.src : book.coverUrl}
                                    width={150} height={200} alt={book.title} className="rounded-md object-contain md:object-cover" />
                            </div>
                            <p className="font-bold mt-2 text-center">{book.title}</p>
                            <p className="text-sm text-gray-500 text-center">{book.authors?.join(", ")}</p>
                        </CardContent>
                        {(book.rating != null) && (book.ratingCount != null) && (
                            <CardFooter className="justify-center">
                                <StarRating rating={book.rating} />
                                <p className="ml-1">({book.ratingCount})</p>
                            </CardFooter>
                        )}
                    </Card>
                ))
            }
        </div>
    )
}