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

  // Настройка Swagger
  const config = new DocumentBuilder()
    .setTitle('Приют для кошек')
    .setDescription('Система управления кошками и пользователями')
    .setVersion('1.0')
    .addBearerAuth()
    .addTag('auth', 'Авторизация и регистрация')
    .addTag('cats', 'Операции с животными')
    .addTag('users', 'Операции с пользователями')
    .build();
    
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document); // Swagger будет по ссылке /api

  await app.listen(3000);
  console.log(`Приложение запущено на: http://localhost:3000/api`);
}
bootstrap();