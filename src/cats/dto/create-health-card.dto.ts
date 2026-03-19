import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsOptional, IsDateString, IsNotEmpty } from 'class-validator';
import { Transform } from 'class-transformer';

export class CreateHealthCardDto {
  @ApiProperty({ 
    example: '2025-12-01', 
    description: 'Date of the last vaccination' 
  })
  @IsDateString()
  lastVaccination: Date;

  @ApiProperty({ 
    example: 'Healthy', 
    description: 'Current medical status (e.g., Healthy, Under Treatment, Recovering)' 
  })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty()
  medicalStatus: string;

  @ApiProperty({ 
    example: 'Allergic to chicken; needs monthly vitamin drops.', 
    description: 'Special veterinary notes',
    required: false 
  })
  @IsOptional()
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  notes?: string;
}