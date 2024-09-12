import path from 'path'
import promises from 'fs/promises'
import { Worker, parentPort, workerData } from 'worker_threads'
import { extractFeatureFromPackage } from '../../feature-extract'
import { getErrorInfo } from '../../util'
import { getConfig } from '../../config'
import { Logger } from '../../Logger'
import { readdirSync } from 'fs'

/**
 * Get the result of extracting features
 * @param fileName the name of the npm package
 * @param featurePosPath the absolute path to the feature position file
 * @returns the result of extracting features
 */
function getAnalyzeResult (fileName: string, featurePosPath: string): string {
  return `Finished extracting features of ${fileName}, recorded at ${featurePosPath}`
}

/**
 * Extract the features of a single npm package
 * @param packagePath the absolute path to npm package
 * @param featureDirPath the absolute directory path to save feature files
 * @param featurePosDirPath the absolute directory path to save feature position files
 * @returns the result of extracting features
 */
export async function analyzeSinglePackage (packagePath: string, featureDirPath: string, featurePosDirPath: string) {
  const result = await extractFeatureFromPackage(packagePath, featureDirPath)
  // const packageName = path.basename(path.dirname(packagePath))
  const packageName = path.basename(packagePath)
  try {
    const featurePosPath = path.join(featurePosDirPath, `${packageName}.json`)
    // const featurePosPath = path.join(featurePosDirPath, `feature-positions.json`)
    Logger.info(getAnalyzeResult(packageName, featurePosPath))
    await promises.writeFile(featurePosPath, getConfig().positionRecorder!.serializeRecord())
    return result
  } catch (error) {
    Logger.error(getErrorInfo(error))
    return null
  }
}

/**
 * Extract the features of all npm packages in the directory
 * @param packageDirPath the absolute directory path to npm package
 * @param featureDirPath the absolute directory path to save feature files
 * @param featurePosDirPath the absolute directory path to save feature position files
 */
export async function analyzePackages (packageDirPath: string, featureDirPath: string, featurePosDirPath: string) {
  try { await promises.mkdir(featureDirPath) } catch (e) {}
  try { await promises.mkdir(featurePosDirPath) } catch (e) {}
  // const packagesPath = await getPackagesFromDir(packageDirPath)
  let packagesPath: string[] = []
  for (const packagePath of readdirSync(packageDirPath)) {
    if ((await promises.stat(path.join(packageDirPath, packagePath))).isDirectory()) {
      packagesPath.push(path.join(packageDirPath, packagePath))
    }
  }
  return packagesPath
}

export async function analyzePackagesMaster(packagesPath: string[], featureDirPath: string, featurePosDirPath: string) {
  // const workersCount = os.cpus().length
  // FIXME: use 8 workers for now because of the memory limit, or the program will be killed
  const workersCount = 8
  const workload = Math.ceil(packagesPath.length / workersCount)
  const workers: Worker[] = []
  for (let i = 0; i < workersCount; i++) {
    const start = i * workload
    const end = start + workload
    const worker = new Worker(__filename, {
      workerData: {
        workerId: i,
        packagesPath: packagesPath.slice(start, end),
        featureDirPath,
        featurePosDirPath
      }
    })
    workers.push(worker)
  }
  for (const worker of workers) {
    worker.on('exit', (exitCode: number) => {
      Logger.info(`Worker stopped with exit code ${exitCode}`)
    })
  }
}

export async function analyzePackagesWorker() {
  const { workerId, packagesPath, featureDirPath, featurePosDirPath } = workerData
  Logger.info(`Worker ${workerId} started`)
  for (const packagePath of packagesPath) {
    await analyzeSinglePackage(packagePath, featureDirPath, featurePosDirPath)
  }
  Logger.info(`Worker ${workerId} finished`)
  if (parentPort) {
    parentPort.postMessage(`Worker ${workerId} finished`)
  }
}