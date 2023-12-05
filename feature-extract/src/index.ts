import { accessSync, constants } from 'fs'
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads'
import { Logger } from './Logger'
import { analyzeSinglePackage, analyzePackages, analyzePackagesMaster, analyzePackagesWorker } from './programs/AnalyzePackage/PackageAnalyzer'

function showUsage () {
  Logger.info(
`node main.js [-p, -d] [$package_path, $package_dir_path] $feature_dir_path $feature_pos_dir_path.
\t$package_path is absolute path to the npm package which should have a file named package.json.
\t$package_dir_path is absolute path to the parent directory of the npm package which should have a file named package.json.
\t$feature_dir_path is absolute path to the parent directory of the feature files.
\t$feature_pos_dir_path is absolute path to the parent directory of the feature position files.`
  )
}

async function main () {
  if (process.argv.length === 6) {
    const option = process.argv[2]
    const packageOrDirPath = process.argv[3]
    const featureDirPath = process.argv[4]
    const featurePosDirPath = process.argv[5]
    try {
      if (option === '-d') {
        accessSync(packageOrDirPath, constants.F_OK | constants.R_OK)
        const packagesPath = await analyzePackages(packageOrDirPath, featureDirPath, featurePosDirPath)
        await analyzePackagesMaster(packagesPath, featureDirPath, featurePosDirPath)
        return
      } else if (option === '-p') {
        accessSync(packageOrDirPath, constants.F_OK | constants.R_OK)
        await analyzeSinglePackage(packageOrDirPath, featureDirPath, featurePosDirPath)
      } else {
        throw new Error('Invalid option. Please use -p or -d.')
      }
    } catch (error) {
      Logger.error(`Error: ${(error as Error).message}`)
      Logger.error(`Stack: ${(error as Error).stack}`)
    }
  } else {
    showUsage()
  }
}

if (isMainThread) {
  main()
} else {
  analyzePackagesWorker()
}
