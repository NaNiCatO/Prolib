"use client"

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { PlusCircle } from "lucide-react";
import Image from "next/image";
import { redirect } from "next/navigation";
import { AddBookData } from "../lib/types";
import { camelCaseToWords } from "@/lib/utils";
import { Textarea } from "@/components/ui/textarea";
import CategorySelectionBadges from "../ui/category-selection-badges";
import { makeAPIFromAddBookData } from "../lib/bookDataFormatting";

const defaultFormState: AddBookData = {
    title: "",
    authors: [],
    categories: [],
    description: "",
    publisher: "",
    publishedDate: "",
    language: "",
    pageCount: "1",
    coverUrl: ""
}

const AddBookForm = () => {
    const [formData, setFormData] = useState<AddBookData>(defaultFormState);
    const [selectedCategory, setSelectedCategory] = useState("");
    const [coverImage, setCoverImage] = useState<null | File>(null);

    const router = useRouter()

    const handleInputChange = (e: any) => {
        const { name, value } = e.target;
        if (name == "authors") return setFormData((prev) => ({ ...prev, [name]: [value] }));

        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    // const handleGenreChange = (value: string[]) => {
    //     setFormData((prev) => ({ ...prev, categories: value }));
    // };

    const handleSubmit = async (e: any) => {
        e.preventDefault();

        // Save the File glob on local and set path to coverUrl in formData
        let filePath: string = "N/A";
        if (coverImage) {
            const formDataImage = new FormData();
            formDataImage.append('image', coverImage);

            const res1 = await fetch('/api/uploadImage', {
                method: 'POST',
                body: formDataImage,
            });

            filePath = `/uploads/${(await res1.json()).filename}`
        }

        // Set file path
        formData.coverUrl = filePath

        // Join authors with commas as separator
        formData.authors = formData.authors.join("").split(",")

        // Handle form submission here
        const test = JSON.stringify(makeAPIFromAddBookData(formData))
        console.log(test, "add book sent")

        const res2 = await fetch(new URL('http://localhost:8000/books'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(makeAPIFromAddBookData(formData)),
        });

        const resStatus = res2.status
        console.log(resStatus)

        // console.log("Form data:", formData, "Cover image:", coverImage, resStatus);
        // resetForm()
        router.push("/myCatalog")
    };

    const resetForm = () => {
        setCoverImage(null)
        setFormData(defaultFormState)
    }

    // console.log(formData, "formdata")

    return (
        <div className="max-w-4xl mx-auto">
            <form id="addBookForm" onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left side - form fields (2/3 width) */}
                <div className="md:col-span-2 space-y-6">
                    {Object.entries(formData).map(([key, value]) => {
                        if (key == "coverUrl") return null
                        if (key == "authors") return ( // field that explains to add comma for multiple authors 
                            <div className="space-y-2" key={key}>
                                <Label htmlFor={key} key={`${key}Label`} className="text-base font-medium">{camelCaseToWords(key)}</Label>
                                <Input
                                    id={key}
                                    name={key}
                                    key={`${key}Input`}
                                    placeholder="Enter Author names"
                                    value={value}
                                    onChange={handleInputChange}
                                    className="h-10"
                                />
                                <p className="text-sm text-gray-500" key={`${key}P`} >Separate multiple authors with commas (e.g., "J.K. Rowling, John Smith")</p>
                            </div>
                        )
                        if (key == "description") return ( // Return a textarea instead of an input field
                            <div className="space-y-2" key={key}>
                                <Label htmlFor={key} key={`${key}Label`} className="text-base font-medium">{camelCaseToWords(key)}</Label>
                                <Textarea
                                    id={key}
                                    name={key}
                                    key={`${key}TextArea`}
                                    placeholder="Enter book description"
                                    value={value as string}
                                    onChange={handleInputChange}
                                    className="min-h-32"
                                />
                            </div>
                        )
                        if (key == "categories") return <CategorySelectionBadges classNames="space-y-2" key={"categorySelectionBadges"} formData={formData} setFormData={setFormData}
                            selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory} />

                        return <div className="space-y-2" key={key}>
                            <Label htmlFor={key} key={`${key}Label`} className="text-base font-medium">{camelCaseToWords(key)}</Label>
                            <Input
                                id={key}
                                name={key}
                                key={`${key}Input`}
                                placeholder={`Enter ${camelCaseToWords(key)}`}
                                value={value}
                                onChange={handleInputChange}
                                className="h-10"
                            />
                        </div>

                    })}
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
                                    key={"Image"}
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
                                key={"imageInput"}
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
                <div className="md:col-span-3 flex space-x-4 mt-4 mb-8">
                    <Button variant="outline" key={"CancelButton"} onClick={resetForm} type="button" className="w-24">
                        Cancel
                    </Button>
                    <Button type="submit" key={"SaveButton"} className="w-24 bg-orange-500 hover:bg-orange-600">
                        Save
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default AddBookForm;