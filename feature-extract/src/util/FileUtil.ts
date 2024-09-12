import { readFile } from 'fs/promises'

/**
 * Determine whether the file is UTF-8 with BOM encoded
 * @param filePath the path to file to be determined
 * @returns whether the file is UTF-8 with BOM encoded
 */
export async function isUTF8WithBOM(filePath: string) {
    const buffer = await readFile(filePath)
    return buffer.length >= 3 && buffer[0] === 0xEF && buffer[1] === 0xBB && buffer[2] === 0xBF
}

/**
 * Read UTF-8 with BOM encoded files as UTF-8 encoded contents
 * @param filePath the path to be UTF-8 with BOM encoded file
 */
export async function readFileFromUTF8WithBOM(filePath: string) {
    const fileContent = await readFile(filePath, { encoding: 'utf8' })
    const utf8Content = fileContent.replace(/^\uFEFF/, '')
    return utf8Content
}