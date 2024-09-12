import path from 'path'
import promises from 'fs/promises'
import { stringify } from 'csv-stringify/sync'
import { getPackageFeatureInfo, type PackageFeatureInfo } from './PackageFeatureInfo'

/**
 * Extract features from the npm package and save the features to the feature file
 * @param packagePath the directory of the npm package, where there should be a package.json file
 * @param featureDirPath directory of saving feature files
 * @returns the path of the feature file and feature information
 */
export async function extractFeatureFromPackage (packagePath: string, featureDirPath: string) {
  const result: PackageFeatureInfo = await getPackageFeatureInfo(packagePath)
  // const packageName = path.basename(path.dirname(packagePath))
  const packageName = path.basename(packagePath)
  const csvPath = path.join(featureDirPath, `${packageName}.csv`)
  const featureArr: Array<[string, number | boolean]> = []
  featureArr.push(['hasInstallScript', result.includeInstallScript])
  featureArr.push(['includeIP', result.includeIP])
  featureArr.push(['useBase64Conversion', result.useBase64Conversion])
  featureArr.push(['useBase64ConversionInScript', result.useBase64ConversionInScript])
  featureArr.push(['includeBase64String', result.includeBase64String])
  featureArr.push(['includeBase64StringInScript', result.includeBase64StringInScript])
  featureArr.push(['includeByteString', result.includeByteString])
  featureArr.push(['includeDomain', result.includeDomain])
  featureArr.push(['includeDomainInScript', result.includeDomainInScript])
  featureArr.push(['useBuffer', result.useBuffer])
  featureArr.push(['useEval', result.useEval])
  featureArr.push(['useProcess', result.useProcess])
  featureArr.push(['useProcessInScript', result.useProcessInScript])
  featureArr.push(['useFileSystem', result.useFileSystem])
  featureArr.push(['useFileSystemInScript', result.useFileSystemInScript])
  featureArr.push(['useNetwork', result.useNetwork])
  featureArr.push(['useNetworkInScript', result.useNetworkInScript])
  featureArr.push(['useProcessEnv', result.useProcessEnv])
  featureArr.push(['useProcessEnvInScript', result.useProcessEnvInScript])
  featureArr.push(['containSuspicousString', result.includeSensitiveFiles])
  featureArr.push(['useEncryptAndEncode', result.useEncryptAndEncode])
  featureArr.push(['useOperatingSystem', result.useOperatingSystem])
  featureArr.push(['includeObfuscatedCode', result.includeObfuscatedCode])
  await new Promise(resolve => {
    setTimeout(async () => {
      await promises.writeFile(csvPath, stringify(featureArr, {
        cast: {
          boolean: function (value) {
            if (value) {
              return 'true'
            }
            return 'false'
          }
        }
      }))
      resolve(true)
    })
  })
  return {
    csvPath,
    featureInfo: result
  }
}
