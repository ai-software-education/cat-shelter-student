import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsInt, IsOptional, Min, MinLength, IsNotEmpty } from 'class-validator';
import { Transform } from 'class-transformer';

export class CreateCatDto {
  @ApiProperty({ 
    example: 'Barsik', 
    description: 'The official name of the cat for registration',
    minLength: 2 
  })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty({ message: 'Name should not be empty or contain only spaces' })
  @MinLength(2)
  name: string;

  @ApiProperty({ 
    example: 2, 
    description: 'Age of the cat in years',
    minimum: 0 
  })
  @IsInt()
  @Min(0)
  age: number;

  @ApiProperty({ 
    example: 'Siamese', 
    description: 'Breed or closest phenotype' 
  })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty({ message: 'Breed should not be empty' })
  breed: string;

  @ApiProperty({ 
    example: 'Found in a park during winter 2024', 
    description: 'Background story of how the cat arrived at the shelter',
    required: false 
  })
  @IsOptional()
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  history?: string;

  @ApiProperty({ 
    example: 'A very friendly and playful cat, loves children.', 
    description: 'Detailed characteristic or personality description',
    required: false 
  })
  @IsOptional()
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  description?: string;
}