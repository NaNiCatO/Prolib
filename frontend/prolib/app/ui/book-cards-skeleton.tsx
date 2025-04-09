import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function BookCardSkeleton({ count = 20 }: { count?: number }) {
    return (
        <>
            {Array.from({ length: count }).map((_, index) => (
                <Card key={index} className="shadow-md w-52 select-none">
                    <CardContent>
                        <div className="flex justify-center w-full h-52 pt-4">
                            <Skeleton className="h-48 w-36 rounded-md" />
                        </div>
                        <div className="mt-2 space-y-2">
                            <Skeleton className="h-5 w-full" />
                            <Skeleton className="h-4 w-3/4 mx-auto" />
                        </div>
                    </CardContent>
                    <CardFooter className="justify-center">
                        <div className="flex items-center">
                            <div className="flex">
                                {Array.from({ length: 5 }).map((_, i) => (
                                    <Skeleton key={i} className="h-4 w-4 mr-1" />
                                ))}
                            </div>
                            <Skeleton className="h-4 w-6 ml-1" />
                        </div>
                    </CardFooter>
                </Card>
            ))}
        </>
    );
}