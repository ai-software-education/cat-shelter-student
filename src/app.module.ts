import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CatsModule } from './cats/cats.module';
import { CatEntity } from './cats/entities/cat.entity';


@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5433,
      username: 'user',
      password: 'password',
      database: 'shelter',
      entities: [CatEntity],
      synchronize: true,
    }),
    CatsModule,
  ],
})
export class AppModule {}