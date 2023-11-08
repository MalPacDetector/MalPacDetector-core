import { type PackageFeatureInfo } from './PackageFeatureInfo'

const MAX_RECORD_NUMBER = 1000

export interface Record {
  filePath: string
  content: {
    start: {
      line: number
      column: number
    }
    end: {
      line: number
      column: number
    }
  } | string
}

type RecordFeatureInfo = Omit<PackageFeatureInfo, 'includeBase64String' | 'includeBase64StringInScript' | 'installCommand' | 'executeJSFiles' | 'packageName' | 'version'>

export class PositionRecorder {
  featurePosSet: { [k in keyof RecordFeatureInfo]: Record[] } = {
    includeInstallScript: [],
    includeIP: [],
    useBase64Conversion: [],
    useBase64ConversionInScript: [],
    includeDomain: [],
    includeDomainInScript: [],
    includeByteString: [],
    useBuffer: [],
    useEval: [],
    useProcess: [],
    useProcessInScript: [],
    useFileSystem: [],
    useFileSystemInScript: [],
    useNetwork: [],
    useNetworkInScript: [],
    useProcessEnv: [],
    useProcessEnvInScript: [],
    useEncryptAndEncode: [],
    useOperatingSystem: [],
    includeSensitiveFiles: []
  }

  addRecord (key: keyof PackageFeatureInfo, record: Record) {
    if (this.featurePosSet[key].length > MAX_RECORD_NUMBER) {
      return
    }
    this.featurePosSet[key].push(record)
  }

  serializeRecord () {
    return JSON.stringify(this.featurePosSet)
  }
}
