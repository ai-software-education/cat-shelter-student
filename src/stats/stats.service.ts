import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CatEntity } from '../cats/entities/cat.entity';

@Injectable()
export class StatsService {
  constructor(
    @InjectRepository(CatEntity)
    private readonly catRepository: Repository<CatEntity>,
  ) {}

  async getGeneralSummary() {
    const total = await this.catRepository.count();
    const adopted = await this.catRepository.countBy({ isAdopted: true });
    const percentage = total > 0 ? Number(((adopted / total) * 100).toFixed(2)) : 0;
    return {
      totalAnimals: total,
      adoptedCount: adopted,
      adoptionRate: percentage,
    };
  }

  async getBreedDistribution() {
    const rawStats = await this.catRepository
      .createQueryBuilder('cat')
      .select('cat.breed', 'breed')
      .addSelect('COUNT(cat.id)', 'count')
      .groupBy('cat.breed')
      .orderBy('count', 'DESC')
      .getRawMany();
    return rawStats.map(item => ({
      breed: item.breed,
      count: Number(item.count),
    }));
  }

  async getTopAdopters() {
    const rawAdopters = await this.catRepository
      .createQueryBuilder('cat')
      .innerJoin('cat.owner', 'user')
      .select([
        'user.id AS id',
        'user.firstName AS firstName',
        'user.lastName AS lastName',
      ])
      .addSelect('COUNT(cat.id)', 'count')
      .groupBy('user.id')
      .orderBy('count', 'DESC')
      .limit(5)
      .getRawMany();
    return rawAdopters.map(adopter => ({
      id: Number(adopter.id),
      firstName: adopter.firstName,
      lastName: adopter.lastName,
      count: Number(adopter.count),
    }));
  }
}