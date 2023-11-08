import { type PositionRecorder } from './feature-extract/PositionRecorder'

export enum Classifier {
  RF = 'RF',
  SVM = 'SVM',
  NB = 'NB',
  MLP = 'MLP',
}

interface Config {
  positionRecorder: PositionRecorder | null
  classifier: Classifier
}

const config: Config = {
  positionRecorder: null,
  classifier: Classifier.SVM
}

export const getConfig = () => config

export const setPositionRecorder = (positionRecorder: PositionRecorder) => {
  config.positionRecorder = positionRecorder
}

export const setClassifier = (classifier: Classifier) => {
  config.classifier = classifier
}
