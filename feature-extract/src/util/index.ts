import fs, { readdirSync } from 'fs'
import path, { basename, join } from 'path'

export function getRootDirectory () {
  if (isProduction()) {
    return __dirname
  }
  const currentFilePath = process.argv[1]
  let projectRootPath = currentFilePath

  while (!fs.existsSync(path.join(projectRootPath, 'package.json'))) {
    projectRootPath = path.dirname(projectRootPath)
  }

  return projectRootPath
}

/**
 * Get the actual package path from a directory. 
 * It is considered that the directory where the package.json file is located is the actual directory of the package,
 * and if there are multiple package.json files, the lower level of the directory is the actual directory of the package.
 * 
 * Example:
 * 
 * Common package directory structure:
 * package_name
 *   package
 *     ├── package.json
 * We consider the directory 'package' as the actual directory of the package.
 * 
 * Sometimes the package directory structure is as follows:
 * package_name
 *  other_name
 *    ...
 *      actual_package
 *        ├── package.json
 * We consider the directory 'actual_package' as the actual directory of the package.
 * 
 * @param packageDirPath the path to the directory to be searched
 * @returns all pakcages in the directory
 */
export async function getPackageFromDir(packageDirPath: string) {
  let result = ''
  async function resolve(dirPath: string) {
    const fileAndDirs = readdirSync(dirPath, { withFileTypes: true })
    const files = fileAndDirs.filter(fileOrDir => fileOrDir.isFile())
    const dirs = fileAndDirs.filter(fileOrDir => fileOrDir.isDirectory())
    for (const file of files) {
      if (file.name === 'package.json') {
        result = dirPath
        return
      }
    }
    for (const dir of dirs) {
      if (dir.name !== 'node_modules') {
        await resolve(join(dirPath, dir.name))
      }
    }
  }
  await resolve(packageDirPath)
  return result
}

/**
 * Get all packages from a directory. 
 * It is considered that the directory where the package.json file is located is the actual directory of the package,
 * and if there are multiple package.json files, the lower level of the directory is the actual directory of the package.
 * @param packageDirPath the path to the directory to be searched
 * @returns all pakcages in the directory
 */
export async function getPackagesFromDir (packageDirPath: string) {
  const result: string[] = []
  async function resolve (dirPath: string) {
    const fileAndDirs = readdirSync(dirPath, { withFileTypes: true })
    const files = fileAndDirs.filter(fileOrDir => fileOrDir.isFile())
    const dirs = fileAndDirs.filter(fileOrDir => fileOrDir.isDirectory())
    for (const file of files) {
      if (file.name === 'package.json') {
        result.push(dirPath)
        return
      }
    }
    for (const dir of dirs) {
      if (dir.name !== 'node_modules') {
        await resolve(join(dirPath, dir.name))
      }
    }
  }
  await resolve(packageDirPath)
  return result
}

/**
 * Get the valid file name.
 * @param fileName the file name to be checked
 * @returns a valid file name string and replaces all / in fileName with #
 */
export function getValidFileName (fileName: string) {
  return fileName.replace('/', '#')
}

export function getErrorInfo (error: Error) {
  // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
  return `error name: ${error.name}\nerror message: ${error.message}\nerror stack: ${error.stack}`
}

export function isProduction () {
  return !!process.env.NODE_ENV
}
