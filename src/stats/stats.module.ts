import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { StatsController } from './stats.controller';
import { StatsService } from './stats.service';
import { CatEntity } from '../cats/entities/cat.entity';
import { UserEntity } from '../users/entities/user.entity';

@Module({
  imports: [TypeOrmModule.forFeature([CatEntity, UserEntity])],
  controllers: [StatsController],
  providers: [StatsService],
})
export class StatsModule {}