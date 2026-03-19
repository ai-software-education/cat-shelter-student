import { Entity, PrimaryGeneratedColumn, Column, OneToMany, ManyToOne } from 'typeorm';
import { CatEntity } from 'src/cats/entities/cat.entity';
import { Role } from 'src/roles/entities/role.entity';

@Entity('users')
export class UserEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  login: string;

  @Column({ select: false })
  password: string;

  @Column()
  firstName: string;

  @Column()
  lastName: string;

  @OneToMany(() => CatEntity, (cat) => cat.owner)
  cats: CatEntity[];

  @ManyToOne(() => Role)
  role: Role;
}