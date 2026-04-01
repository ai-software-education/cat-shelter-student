import { Injectable, NotFoundException,  ConflictException} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CatEntity } from './entities/cat.entity';
import { CreateCatDto } from './dto/create-cat.dto';

@Injectable()
export class CatsService {
  constructor(
    @InjectRepository(CatEntity)
    private readonly catRepository: Repository<CatEntity>,
  ) {}

  findAll(): Promise<CatEntity[]> {
    return this.catRepository.find();
  }

  async findOne(id: number): Promise<CatEntity> {
    const cat = await this.catRepository.findOneBy({ id });
    if (!cat) throw new NotFoundException(`Cat with ID ${id} not found`);
    return cat;
  }

  async create(dto: CreateCatDto): Promise<CatEntity> {
    const existing = await this.catRepository.findOneBy({ name: dto.name });
    if (existing) {
      throw new ConflictException(`Cat with name "${dto.name}" already exists`);
    }
    
    const newCat = this.catRepository.create(dto);
    return this.catRepository.save(newCat);
  }

  async remove(id: number): Promise<void> {
    const cat = await this.catRepository.findOneBy({ id });
    if (!cat) {
      throw new NotFoundException(`Cat with ID ${id} not found`);
    }
    await this.catRepository.remove(cat);
  }
}