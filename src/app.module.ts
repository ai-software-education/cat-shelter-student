import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UsersModule } from './users/users.module';
import { CatsModule } from './cats/cats.module';
import { CatEntity } from './cats/entities/cat.entity';
import { UserEntity } from './users/entities/user.entity';
import { StatsModule } from './stats/stats.module';
import { AuthModule } from './auth/auth.module';
import { Role } from './roles/entities/role.entity';
import { HealthCard } from './cats/entities/health-card.entity';


@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DATABASE_HOST || 'localhost', 
      port: parseInt(process.env.DATABASE_PORT, 10) || 5432, 
      username: 'user',
      password: 'password',
      database: 'shelter',
      entities: [CatEntity, UserEntity, Role, HealthCard],
      synchronize: true, 
    }),
    AuthModule,
    CatsModule,
    UsersModule,
    StatsModule,
  ],
})
export class AppModule {}