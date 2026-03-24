import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    transform: true,
    stopAtFirstError: true,
  }));

  const config = new DocumentBuilder()
    .setTitle('Cat Shelter Foundation API')
    .setDescription('Basic system for tracking shelter animals. Assignment #1.')
    .setVersion('1.0')
    .addTag('Cats Management', 'Core operations for cat records')
    .build();
    
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  // Запуск сервера
  await app.listen(3000);
  
  console.log(`---`);
  console.log(`Application is running on: http://localhost:3000/api`);
  console.log(`OpenAPI specification (JSON): http://localhost:3000/api-json`);
  console.log(`---`);
}
bootstrap();