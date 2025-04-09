import { Separator } from '@/components/ui/separator'
import Link from 'next/link'

export default function NotFound() {
    return (
        <div className='flex flex-col justify-center items-center'>
            <h2>Not Found</h2>
            <p>Could not find requested resource</p>
            <Separator />
            <Link href="/">Return Home</Link>
        </div>
    )
}