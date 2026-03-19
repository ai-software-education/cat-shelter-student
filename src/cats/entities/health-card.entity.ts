import { Entity, PrimaryGeneratedColumn, Column, OneToOne, JoinColumn } from 'typeorm';
import { CatEntity } from './cat.entity';

@Entity('health_cards')
export class HealthCard {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  lastVaccination: Date; // Дата последней прививки

  @Column({ default: 'Healthy' })
  medicalStatus: string; // Статус: здоров, на лечении и т.д.

  @Column({ type: 'text', nullable: true })
  notes: string; // Особые заметки ветеринара

  @OneToOne(() => CatEntity, (cat) => cat.healthCard, { onDelete: 'CASCADE' })
  @JoinColumn()
  cat: CatEntity;
}