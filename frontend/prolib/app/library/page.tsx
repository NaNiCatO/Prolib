"use client"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { ChevronDown, CircleUser, Filter, Search, ArrowDownAZ, ArrowUpZA } from "lucide-react";
import Image from "next/image";
import StarRating from "@/app/ui/star-rating";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { FilterSelect } from "../ui/book-filter-select";
import { useState } from "react";

const books = [
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 2.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 0.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 0, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 4.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Garfield", author: "Jim Davis", cover: "/garfield.jpg", rating: 3.5, ratingCount: 17 },
  { title: "Oggy", author: "Jordan Gershowitz", cover: "/oggy.jpg", rating: 3.5, ratingCount: 17 },
];

export default function Library() {
  const [increment, setIncrement] = useState(true)

  const toggleIncrement = () => setIncrement(bool => !bool)

  return (
    <div className="flex flex-col flex-nowrap w-full pl-2.5 pr-2.5">
      {/* {Title and profile icon} */}
      <header className="flex h-12 shrink-0 justify-between justify-items-center items-center gap-2 border-b-2 transition-[width,height] ease-linear">
        <h1 className="m-5 text-4xl">Find a book to read!</h1>

        <Avatar className="w-13 h-13 mb-2 mr-6">
          <AvatarImage />
          <AvatarFallback><CircleUser size={50} /></AvatarFallback>
        </Avatar>
      </header>
      {/* {Search and filters} */}
      <div className="m-7 flex flex-nowrap justify-between items-center">
        <div className="relative basis-2/3 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={17} />
          <Input
            type="text"
            placeholder="Search books..."
            className="w-full min-w-xs rounded-lg pl-10"
          />
        </div>
        <div className="flex justify-between basis-1/3 ml-2">
          {/* <Button variant="outline" className="grow m-1">
            Cover <ChevronDown size={16} />
          </Button> */}
          {/* <Button variant="outline" className="grow m-1">
            Title <ChevronDown size={16} />
          </Button> */}
          <FilterSelect className="grow m-1" />
          <Button variant="outline" className="m-1" size={"icon"} onClick={toggleIncrement}>
            {increment ? <ArrowDownAZ /> : <ArrowUpZA />}
          </Button>
          <Button variant="default" className="grow m-1">
            <Filter size={16} className="mr-2" /> Filter
          </Button>
        </div>

      </div>
      {/* {Book Cards} */}
      <div className="ml-4 mr-4 flex flex-wrap justify-start gap-4">
        {books.map((book) => (
          <Card key={book.title} className="shadow-md w-52">
            <CardContent>
              <div className="flex justify-center w-full h-52">
                <Image src={book.cover} width={150} height={200} alt={book.title} className="rounded-md object-contain md:object-cover" />
              </div>
              <p className="font-bold mt-2 text-center">{book.title}</p>
              <p className="text-sm text-gray-500 text-center">{book.author}</p>
            </CardContent>
            <CardFooter className="justify-center">
              <StarRating rating={book.rating} />
              <p className="ml-1">({book.ratingCount})</p>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
