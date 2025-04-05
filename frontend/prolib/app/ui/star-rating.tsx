import { Star, StarHalf } from "lucide-react";

const StarRating = ({ rating, maxRating = 5 }: { rating: number, maxRating?: number }) => {
    // Convert rating to a number and ensure it's within bounds
    const numRating = Math.min(Math.max(0, rating), maxRating);

    // Calculate full and half stars
    const fullStars = Math.floor(numRating);
    const hasHalfStar = numRating % 1 >= 0.5;

    return (
        <div className="flex">
            {Array.from({ length: maxRating }).map((_, i) => {
                // Full star
                if (i < fullStars) {
                    return <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />;
                }
                // Half star
                else if (i === fullStars && hasHalfStar) {
                    return (
                        <div key={i} className="relative w-4 h-4">
                            <Star className="absolute w-4 h-4 text-yellow-400" />
                            <StarHalf className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        </div>
                    );
                }
                // Empty star
                else {
                    return <Star key={i} className="w-4 h-4 text-yellow-400" />;
                }
            })}
        </div>
    );
};

export default StarRating;