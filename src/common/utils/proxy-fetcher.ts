import { HttpException } from '@nestjs/common';

const GO_SERVICE_URL = process.env.GO_SERVICE_URL || 'http://cat-reader:8080';

export async function proxyGet(path: string) {
  const response = await fetch(`${GO_SERVICE_URL}${path}`);

  const data = await response.json();

  if (!response.ok) {
    throw new HttpException(
      data.message || 'Reader service error',
      response.status,
    );
  }

  return data;
}