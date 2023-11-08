/* eslint-disable no-useless-catch */
import { parse } from '@babel/core'
import traverse from '@babel/traverse'
import { accessSync, readFileSync } from 'fs'
import { dirname, join } from 'path'
import { isStringLiteral } from '@babel/types'
import { getFileLogger } from '../FileLogger'

/**
 * Get all JavaScript files that are executed or imported directly and indirectly in the install hook
 * @param jsFilesInInstallScript the path to js files in install script
 * @returns the parameter jsFilesInInstallScript
 */
export async function getAllJSFilesInInstallScript (jsFilesInInstallScript: string[]) {
  async function resolveAllJSFilesInInstallScript (jsFilesInInstallScript: string[], idx: number) {
    if (idx >= jsFilesInInstallScript.length) {
      return
    }
    const logger = await getFileLogger()
    const codeContent = readFileSync(jsFilesInInstallScript[idx], {
      encoding: 'utf-8'
    })
    let ast: any
    try {
      ast = parse(codeContent, {
        sourceType: 'unambiguous'
      })
    } catch (error) {
      await logger.log('Current analyzed file is ' + jsFilesInInstallScript[idx])
      const errorObj = error as Error
      await logger.log(`ERROR MESSAGE: ${errorObj.name}: ${errorObj.message}`)
      await logger.log('ERROR STACK:' + errorObj.stack)
    }
    try {
      traverse(ast, {
        CallExpression: function (path) {
          // @ts-expect-error uselesss lint error
          if (path.node.callee.name === 'require') {
            if (path.node.arguments.length > 0) {
              if (isStringLiteral(path.node.arguments[0])) {
                const moduleName = path.node.arguments[0].value
                try {
                  if (moduleName.startsWith('/') || moduleName.startsWith('./') || moduleName.startsWith('../')) {
                    let importScript = join(dirname(jsFilesInInstallScript[idx]), moduleName)
                    if (importScript.endsWith('.js') || !importScript.includes('.')) {
                      if (!importScript.endsWith('.js')) {
                        importScript = importScript + '.js'
                      }
                      try {
                        accessSync(importScript)
                        jsFilesInInstallScript.push(importScript)
                      } catch (error) {
                        console.log(error)
                      }
                    }
                  }
                } catch (error) {
                  throw error
                }
              }
            }
          }
        }
      })
    } catch (error) {
      await logger.log('Current analyzed file is ' + jsFilesInInstallScript[idx])
      const errorObj = error as Error
      await logger.log(`ERROR MESSAGE: ${errorObj.name}: ${errorObj.message}`)
      await logger.log('ERROR STACK:' + errorObj.stack)
    }
    await resolveAllJSFilesInInstallScript(jsFilesInInstallScript, idx + 1)
  }

  await resolveAllJSFilesInInstallScript(jsFilesInInstallScript, 0)
}
