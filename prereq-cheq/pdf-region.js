import * as pdfjsLib from "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.4.168/build/pdf.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.4.168/build/pdf.worker.mjs";

function assertPositiveNumber(value, name) {
  if (!Number.isFinite(value) || value <= 0) {
    throw new Error(`${name} must be a positive number.`);
  }
}

function assertNonNegativeNumber(value, name) {
  if (!Number.isFinite(value) || value < 0) {
    throw new Error(`${name} must be a non-negative number.`);
  }
}

export async function renderPdfRegionToCanvas({
  file,
  pageNumber,
  x,
  y,
  width,
  height,
  scale = 2,
  canvas
}) {
  if (!file) {
    throw new Error("file is required.");
  }
  assertPositiveNumber(pageNumber, "pageNumber");
  assertNonNegativeNumber(x, "x");
  assertNonNegativeNumber(y, "y");
  assertPositiveNumber(width, "width");
  assertPositiveNumber(height, "height");
  assertPositiveNumber(scale, "scale");

  const outputCanvas = canvas || document.createElement("canvas");
  const outputContext = outputCanvas.getContext("2d");
  if (!outputContext) {
    throw new Error("Could not create a 2D canvas context.");
  }

  const loadingTask = pdfjsLib.getDocument(file);
  const pdf = await loadingTask.promise;
  const page = await pdf.getPage(pageNumber);
  const viewport = page.getViewport({ scale });

  const fullCanvas = document.createElement("canvas");
  const fullContext = fullCanvas.getContext("2d");
  if (!fullContext) {
    throw new Error("Could not create an offscreen 2D canvas context.");
  }

  fullCanvas.width = Math.ceil(viewport.width);
  fullCanvas.height = Math.ceil(viewport.height);

  await page.render({
    canvasContext: fullContext,
    viewport
  }).promise;

  const cropX = Math.round(x * scale);
  const cropWidth = Math.round(width * scale);
  const cropHeight = Math.round(height * scale);
  const cropY = Math.round(viewport.height - ((y + height) * scale));

  outputCanvas.width = cropWidth;
  outputCanvas.height = cropHeight;
  outputContext.clearRect(0, 0, cropWidth, cropHeight);
  outputContext.drawImage(
    fullCanvas,
    cropX,
    cropY,
    cropWidth,
    cropHeight,
    0,
    0,
    cropWidth,
    cropHeight
  );

  return outputCanvas;
}

export async function createPdfRegionCanvas(options) {
  return renderPdfRegionToCanvas(options);
}
