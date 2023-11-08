import { type FileHandle, open, mkdir } from 'fs/promises'
import { dirname, join } from 'path'
import { getRootDirectory } from './util'

export class FileLogger {
  fileHandler: FileHandle
  
  async init (logFilePath: string) {
    try {
      await mkdir(dirname(logFilePath), { recursive: true })
    } catch (e) {

    }

    this.fileHandler = await open(logFilePath, 'w+')
    return this
  }

  async log (message: string) {
    await this.fileHandler.writeFile(message + ' ' + new Date().toLocaleString() + '\n')
  }

  async close () {
    await this.fileHandler.close()
  }
}

let logger: FileLogger | undefined

export async function getFileLogger (): Promise<FileLogger> {
  if (logger != null) {
    return logger
  }
  logger = new FileLogger()
  const logPath = join(getRootDirectory(), 'log', 'error.log')
  await logger.init(logPath)
  return logger
}
