import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsInt, Min, MinLength, IsOptional, IsNotEmpty } from 'class-validator';
import { Transform } from 'class-transformer';

export class CreateCatDto {
  @ApiProperty({ example: 'Barsik', description: 'Name of the cat' })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty({ message: 'Name should not be empty' })
  @MinLength(2)
  name: string;

  @ApiProperty({ example: 2, description: 'Age of the cat' })
  @IsInt()
  @Min(0)
  age: number;

  @ApiProperty({ example: 'Siamese', description: 'Breed of the cat' })
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  @IsNotEmpty({ message: 'Breed should not be empty' })
  breed: string;

  @ApiProperty({ example: 'Found in 2024', required: false })
  @IsOptional()
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  history?: string;

  @ApiProperty({ example: 'Very friendly', required: false })
  @IsOptional()
  @IsString()
  @Transform(({ value }) => (typeof value === 'string' ? value.trim() : value))
  description?: string;
}