"use client"

import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PlusCircle } from "lucide-react";
import Image from "next/image";
import { redirect } from "next/navigation";
import GENRES from "../lib/bookGenres.json"

const AddBookForm = () => {
    const [formData, setFormData] = useState({
        title: "",
        author: "",
        summary: "",
        isbn: "",
        genre: "",
    });

    const [coverImage, setCoverImage] = useState<null | File>(null);

    const handleInputChange = (e: any) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleGenreChange = (value: string) => {
        setFormData((prev) => ({ ...prev, genre: value }));
    };

    const handleSubmit = (e: any) => {
        e.preventDefault();
        // Handle form submission here
        console.log("Form data:", formData, "Cover image:", coverImage);
        resetForm()
        redirect("/myCatalog") // Change this to useRouter instead
    };

    const resetForm = () => {
        setCoverImage(null)
        setFormData({
            title: "",
            author: "",
            summary: "",
            isbn: "",
            genre: "",
        })
    }


    return (
        <div className="max-w-4xl mx-auto">
            <form id="addBookForm" onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left side - form fields (2/3 width) */}
                <div className="md:col-span-2 space-y-6">
                    {/* Book Title */}
                    <div className="space-y-2">
                        <Label htmlFor="title" className="text-base font-medium">Book Title</Label>
                        <Input
                            id="title"
                            name="title"
                            placeholder="Enter book title"
                            value={formData.title}
                            onChange={handleInputChange}
                            className="h-10"
                        />
                    </div>

                    {/* Author */}
                    <div className="space-y-2">
                        <Label htmlFor="author" className="text-base font-medium">Author</Label>
                        <Input
                            id="author"
                            name="author"
                            placeholder="Author's name"
                            value={formData.author}
                            onChange={handleInputChange}
                            className="h-10"
                        />
                    </div>

                    {/* Summary */}
                    <div className="space-y-2">
                        <Label htmlFor="summary" className="text-base font-medium">Summary</Label>
                        <Input
                            id="summary"
                            name="summary"
                            placeholder="Short summary"
                            value={formData.summary}
                            onChange={handleInputChange}
                            className="h-10"
                        />
                    </div>

                    {/* ISBN */}
                    <div className="space-y-2">
                        <Label htmlFor="isbn" className="text-base font-medium">ISBN</Label>
                        <Input
                            id="isbn"
                            name="isbn"
                            placeholder="ISBN (Optional)"
                            value={formData.isbn}
                            onChange={handleInputChange}
                            className="h-10"
                        />
                    </div>

                    {/* Genre */}
                    <div className="space-y-2">
                        <Label htmlFor="genre" className="text-base font-medium">Genre</Label>
                        <Select name="genre" value={formData.genre} onValueChange={handleGenreChange}>
                            <SelectTrigger className="h-10">
                                <SelectValue placeholder="Select Genre" />
                            </SelectTrigger>
                            <SelectContent>
                                {GENRES.map(genre => <SelectItem value={genre.value} id={genre.value} key={genre.value} >{genre.name}</SelectItem>)}
                            </SelectContent>
                        </Select>
                    </div>
                </div>

                {/* Right side - cover image upload (1/3 width) */}
                <div className="md:col-span-1">
                    <div className="flex flex-col items-center">
                        <div
                            className="relative w-full aspect-[3/4] bg-gray-100 rounded-md flex flex-col items-center justify-center border border-dashed border-gray-300"
                            onClick={() => document.getElementById('cover-upload')?.click()}
                        >
                            {coverImage ? (
                                <Image
                                    src={URL.createObjectURL(coverImage)}
                                    alt="Book cover preview"
                                    fill={true}
                                    className="w-full h-full object-cover rounded-md"
                                />
                            ) : (
                                <div className="flex flex-col items-center justify-center h-full w-full">
                                    <PlusCircle className="h-8 w-8 text-gray-400" />
                                    <span className="text-sm text-gray-500 mt-2">Add Cover</span>
                                </div>
                            )}
                            <Input
                                id="cover-upload"
                                type="file"
                                accept="image/*"
                                className="hidden"
                                onChange={(e) => {
                                    if (e.target.files) return setCoverImage(e.target.files[0])
                                }}
                            />
                        </div>
                    </div>
                </div>

                {/* Buttons - full width */}
                <div className="md:col-span-3 flex space-x-4 mt-4">
                    <Button variant="outline" onClick={resetForm} type="button" className="w-24">
                        Cancel
                    </Button>
                    <Button type="submit" className="w-24 bg-orange-500 hover:bg-orange-600">
                        Save
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default AddBookForm;