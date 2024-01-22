import path from 'path'
import promises from 'fs/promises'
import { getPackageJSONInfo, type PackageJSONInfo } from './PackageJSONInfo'
import { getDomainPattern, IP_Pattern, Network_Command_Pattern, SensitiveStringPattern, getDomainsType } from './Patterns'
import { getAllJSFilesInInstallScript } from './GetInstallScripts'
import { extractFeaturesFromJSFileByAST } from './AST'
import { matchUseRegExp } from './RegExp'
import { PositionRecorder } from './PositionRecorder'
import { setPositionRecorder } from '../config'
import { getPackageFromDir } from '../util'
import { Logger } from '../Logger'

const ALLOWED_MAX_JS_SIZE = 2 * 1024 * 1024

export interface PackageFeatureInfo {
  includeInstallScript: boolean
  includeIP: boolean
  useBase64Conversion: boolean
  useBase64ConversionInScript: boolean
  includeBase64String: boolean
  includeBase64StringInScript: boolean
  includeDomain: number
  includeDomainInScript: number
  includeByteString: boolean
  useBuffer: boolean
  useEval: boolean
  useProcess: boolean
  useProcessInScript: boolean
  useFileSystem: boolean
  useFileSystemInScript: boolean
  useNetwork: boolean
  useNetworkInScript: boolean
  useProcessEnv: boolean
  useProcessEnvInScript: boolean
  useEncryptAndEncode: boolean
  useOperatingSystem: boolean
  includeObfuscatedCode: boolean
  includeSensitiveFiles: boolean
  installCommand: string[]
  executeJSFiles: string[]
}

/**
 * Extract features from the npm package
 * @param packagePath the directory of the npm package, where there should be a package.json file
 */
export async function getPackageFeatureInfo (packagePath: string): Promise<PackageFeatureInfo> {
  const positionRecorder = new PositionRecorder()
  const result: PackageFeatureInfo = {
    includeInstallScript: false,
    includeIP: false,
    useBase64Conversion: false,
    useBase64ConversionInScript: false,
    includeBase64String: false,
    includeBase64StringInScript: false,
    includeByteString: false,
    includeDomain: 0,
    includeDomainInScript: 0,
    useBuffer: false,
    useEval: false,
    useProcess: false,
    useProcessInScript: false,
    useFileSystem: false,
    useFileSystemInScript: false,
    useNetwork: false,
    useNetworkInScript: false,
    useProcessEnv: false,
    useProcessEnvInScript: false,
    useEncryptAndEncode: false,
    useOperatingSystem: false,
    includeObfuscatedCode: false,
    includeSensitiveFiles: false,
    installCommand: [],
    executeJSFiles: [],
  }
  
  try {
    // const packageJSONPath = path.join(packagePath, 'package', 'package.json')
    const actualPackagePath = await getPackageFromDir(packagePath)
    if (actualPackagePath !== '') {
      const packageJSONPath = path.join(actualPackagePath, 'package.json')
      await promises.access(packageJSONPath)
      const packageJSONInfo: PackageJSONInfo = await getPackageJSONInfo(packageJSONPath)
      Object.assign(result, packageJSONInfo)

      if (packageJSONInfo.includeInstallScript) {
        positionRecorder.addRecord('includeInstallScript', {
          filePath: packageJSONPath,
          content: packageJSONInfo.installCommand[0]
        })
      }

      // analyze commands in the install script 
      for (const scriptContent of packageJSONInfo.installCommand) {
        {
          const matchResult = scriptContent.match(IP_Pattern)
          if (matchResult != null) {
            result.includeIP = true
            positionRecorder.addRecord('includeIP', { filePath: packageJSONPath, content: scriptContent })
          }
        }
        {
          const matchResult = scriptContent.match(getDomainPattern())
          if (matchResult != null) {
            const domainType = getDomainsType(matchResult)
            if (result.includeDomainInScript < domainType) {
              result.includeDomainInScript = domainType
            }
            for (const domain of matchResult) {
              positionRecorder.addRecord('includeDomainInScript', {
                filePath: packageJSONPath,
                content: domain
              })
            }
          }
        }
        {
          const matchResult = scriptContent.match(Network_Command_Pattern)
          if (matchResult != null) {
            result.useNetworkInScript = true
            positionRecorder.addRecord('useNetworkInScript', {
              filePath: packageJSONPath,
              content: scriptContent
            })
          }
        }
        {
          const matchResult = scriptContent.match(SensitiveStringPattern)
          if (matchResult != null) {
            result.includeSensitiveFiles = true
            positionRecorder.addRecord('includeSensitiveFiles', {
              filePath: packageJSONPath,
              content: scriptContent
            })
          }
        }
      }
    }
    
  } catch (error) {
    Logger.error(`Cannot find package.json in ${packagePath}/package`)
  }

  // analyze JavaScript files in the install script
  await getAllJSFilesInInstallScript(result.executeJSFiles)

  async function traverseDir (dirPath: string) {
    if (path.basename(dirPath) === 'node_modules') {
      return
    }
    const dir = await promises.opendir(dirPath)
    for await (const dirent of dir) {
      const jsFilePath = path.join(dirPath, dirent.name)
      const isInstallScriptFile = result.executeJSFiles.findIndex(filePath => filePath === jsFilePath) >= 0
      if (dirent.isFile() && (dirent.name.endsWith('.js') || isInstallScriptFile)) {
        await new Promise((resolve) => {
          setTimeout(async () => {
            const targetJSFilePath = path.join(dirPath, dirent.name)
            const jsFileContent = await promises.readFile(targetJSFilePath, { encoding: 'utf-8' })
            const fileInfo = await promises.stat(targetJSFilePath)
            if (fileInfo.size <= ALLOWED_MAX_JS_SIZE) {
              await extractFeaturesFromJSFileByAST(jsFileContent, result, isInstallScriptFile, targetJSFilePath, positionRecorder)
              matchUseRegExp(jsFileContent, result, positionRecorder, targetJSFilePath)
            }
            resolve(true)
          }, 0)
        })
      } else if (dirent.isDirectory()) {
        await traverseDir(path.join(dirPath, dirent.name))
      }
    }
  }
  await traverseDir(packagePath)
  setPositionRecorder(positionRecorder)
  return result
}
