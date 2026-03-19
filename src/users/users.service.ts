import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { UserEntity } from './entities/user.entity';
import { Role } from 'src/roles/entities/role.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(UserEntity)
    private readonly userRepository: Repository<UserEntity>,
  ) {}

  async create(dto: any) {
    const user = this.userRepository.create(dto);
    return await this.userRepository.save(user);
  }

  async changeRole(id: number, role: Role) {
    const user = await this.findOne(id);
    user.role = role;
    return await this.userRepository.save(user);
  }

  findAll() {
    return this.userRepository.find();
  }

  async findOne(id: number) {
    const user = await this.userRepository.findOneBy({ id });
    if (!user) throw new NotFoundException('Пользователь не найден');
    return user;
  }

  async remove(id: number) {
    const user = await this.findOne(id);
    await this.userRepository.remove(user);
  }

  async findUserCats(userId: number): Promise<UserEntity> {
    const user = await this.userRepository.findOne({
      where: { id: userId },
      relations: ['cats'],
    });
  
    if (!user) {
      throw new NotFoundException(`User with ID ${userId} not found`);
    }
  
    return user;
  }

  async findByLogin(login: string) {
    return this.userRepository.findOne({ 
      where: { login },
      relations: ['role'],
      select: {
        id: true,
        login: true,
        password: true,
        firstName: true,
        lastName: true,
      }
    });
  }
}