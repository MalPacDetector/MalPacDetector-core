import chalk from 'chalk'

export const Logger = {
  info (message: string) {
    console.log(chalk.green(`${new Date().toLocaleString()}: ${message}\n`))
  },
  warning (message: string) {
    console.log(chalk.yellow(`${new Date().toLocaleString()}: ${message}\n`))
  },
  error (message: string) {
    console.log(chalk.red(`${new Date().toLocaleString()}: ${message}\n`))
  }
}
