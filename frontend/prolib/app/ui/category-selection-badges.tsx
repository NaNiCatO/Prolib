import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, X } from "lucide-react";
import GENRES from "@/app/lib/bookGenres.json"
import { AddBookData, BookEditable } from "../lib/types";
import { Dispatch } from "react";

export default function CategorySelectionBadges({ formData, setFormData, selectedCategory, setSelectedCategory, classNames }:
    { formData: any, setFormData: any, selectedCategory: string, setSelectedCategory: Dispatch<string>, classNames: string }) {

    const handleAddCategory = () => {
        if (selectedCategory && !formData.categories.includes(selectedCategory)) {
            setFormData((oldFormData: any) => ({
                ...oldFormData,
                categories: [...oldFormData.categories, selectedCategory]
            }));
            setSelectedCategory("");
        }
    };

    const handleRemoveCategory = (category: string) => {
        setFormData((oldFormData: any) => ({
            ...oldFormData,
            categories: oldFormData.categories.filter((cat: any) => cat !== category)
        }));
    };

    return (
        <div className={`${classNames}`} key={"categories"}>
            <Label className="text-base font-medium" key="categoriesLabel" >Categories</Label>

            <div className="flex flex-wrap gap-2 mb-2">
                {formData.categories.length > 0 ? (
                    formData.categories.map((category: string) => (
                        <Badge key={category} className="px-3 py-1">
                            {category}
                            <button
                                onClick={() => handleRemoveCategory(category)}
                                className="ml-2 text-xs"
                                key={`${category}Button`}
                            >
                                <X className="h-3 w-3" />
                            </button>
                        </Badge>
                    ))
                ) : (
                    <p className="text-sm text-gray-500" key="categoriesP">No categories selected</p>
                )}
            </div>

            <div className="flex gap-2">
                <Select
                    value={selectedCategory}
                    onValueChange={setSelectedCategory}
                    key="categoriesSelect"
                >
                    <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select a category" />
                    </SelectTrigger>
                    <SelectContent>
                        {GENRES
                            .filter(cat => !formData.categories.includes(cat.name))
                            .map(category => (
                                <SelectItem key={`categoriesSelect${category.value}`} value={category.name}>
                                    {category.name}
                                </SelectItem>
                            ))}
                    </SelectContent>
                </Select>
                <Button
                    type="button"
                    onClick={handleAddCategory}
                    variant="outline"
                    disabled={!selectedCategory}
                    key="categoriesAddButton"
                >
                    <Plus className="h-4 w-4 mr-1" /> Add
                </Button>
            </div>
        </div>
    )
}