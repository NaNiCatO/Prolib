import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import path from 'path';
import { mkdir } from 'fs/promises';
import { randomUUID } from 'crypto';

export async function POST(req: NextRequest) {
    const formData = await req.formData();
    const file = formData.get('image') as File;

    if (!file) {
        return NextResponse.json({ message: 'No file received.' }, { status: 400 });
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    const uploadDir = path.join(process.cwd(), 'public', 'uploads');
    await mkdir(uploadDir, { recursive: true });

    const filename = `${randomUUID()}-${file.name}`;
    const filePath = path.join(uploadDir, filename);

    await writeFile(filePath, buffer);

    return NextResponse.json({ message: 'Image uploaded successfully.', filename });
}
